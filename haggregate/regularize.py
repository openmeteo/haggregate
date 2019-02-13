import numpy as np
import pandas as pd
from htimeseries import HTimeseries


class RegularizeError(Exception):
    pass


def regularize(ts, new_date_flag="DATEINSERT"):
    # Sanity checks
    if not hasattr(ts, "time_step"):
        raise RegularizeError("The source time series does not specify a time step")
    try:
        minutes, months = [int(x.strip()) for x in ts.time_step.split(",")]
        if months or (minutes <= 0):
            raise ValueError()
    except ValueError:
        raise RegularizeError(
            "The time step is malformed or is specified in months. Only time steps "
            "specified in minutes are supported."
        )

    # Set metadata of result
    result = HTimeseries()
    attrs = (
        "unit",
        "time_zone",
        "time_step",
        "interval_type",
        "variable",
        "precision",
        "location",
    )
    for attr in attrs:
        setattr(result, attr, getattr(ts, attr, None))
    result.timestamp_rounding = 0
    result.timestamp_offset = 0
    if hasattr(ts, "title"):
        result.title = "Regularized " + ts.title
    if hasattr(ts, "comment"):
        result.comment = (
            "Created by regularizing step of timeseries that had this comment:\n\n"
            + ts.comment
        )

    # Return immediately if empty
    if len(ts.data) == 0:
        return result

    # Determine first and last timestamps
    freq = ts.time_step.split(",")[0].strip() + "min"
    step = pd.Timedelta(freq)
    first_timestamp_of_result = ts.data.index[0].round(step)
    last_timestamp_of_result = ts.data.index[-1].round(step)

    # Transform all pandas information to plain numpy, which is way faster and is also
    # supported by numba (and Cython)
    orig_index = ts.data.index.values
    orig_values = ts.data["value"].values
    orig_flags = ts.data["flags"].values.astype("U250")
    step = np.timedelta64(step)
    index = pd.date_range(
        first_timestamp_of_result, last_timestamp_of_result, freq=freq
    ).values
    values = np.full(len(index), np.nan, dtype=object)
    flags = np.full(len(index), "", dtype="U250")

    # Do the job
    _perform_regularization(
        index, values, flags, orig_index, orig_values, orig_flags, step, new_date_flag
    )

    result.data = pd.DataFrame(
        index=index,
        columns=["value", "flags"],
        data=np.vstack((values, flags)).transpose(),
    )
    return result


def _perform_regularization(
    index, values, flags, orig_index, orig_values, orig_flags, step, new_date_flag
):
    for i in range(index.size):
        t = index[i]
        values[i], flags[i] = _get_record(
            orig_index, orig_values, orig_flags, t, step, new_date_flag
        )


def _get_record(orig_index, orig_values, orig_flags, t, step, new_date_flag):
    # Return the source record if it already exists
    pos = np.asarray(orig_index == t).nonzero()[0]
    assert pos.size in (0, 1)
    if pos.size == 1:
        i = pos[0]
        return orig_values[i], orig_flags[i]

    # Otherwise get the nearby record, if it exists and is only one
    start = t - step / 2
    end = t + step / 2
    timestamps = np.asarray((orig_index >= start) & (orig_index < end)).nonzero()[0]
    if timestamps.size != 1:
        return np.nan, ""
    i = timestamps[0]
    value = orig_values[i]
    flags = orig_flags[i]
    if flags:
        flags += " "
    flags += "DATEINSERT"
    return value, flags
