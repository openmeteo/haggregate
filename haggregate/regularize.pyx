# cython: language_level=3

cimport numpy as np
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
    # supported by numba and Cython
    ts_index = ts.data.index.values.astype(long)
    ts_values = ts.data["value"].values
    ts_flags = ts.data["flags"].values.astype("U250")
    result_step = np.timedelta64(step).astype(int) * 1000
    result_index = pd.date_range(
        first_timestamp_of_result, last_timestamp_of_result, freq=freq
    ).values
    result_values = np.full(len(result_index), np.nan, dtype=object)
    result_flags = np.full(len(result_index), "", dtype="U250")

    # Do the job
    _perform_regularization(
        result_index,
        result_values,
        result_flags,
        ts_index,
        ts_values,
        ts_flags,
        result_step,
        new_date_flag,
    )

    result.data = pd.DataFrame(
        index=result_index,
        columns=["value", "flags"],
        data=np.vstack((result_values, result_flags)).transpose(),
    )
    return result


def _perform_regularization(
    np.ndarray result_index,
    np.ndarray result_values,
    np.ndarray result_flags,
    np.ndarray ts_index,
    np.ndarray ts_values,
    np.ndarray ts_flags,
    long result_step,
    str new_date_flag,
):
    cdef int i, previous_pos
    cdef long t

    previous_pos = 0
    for i in range(result_index.size):
        t = result_index[i]
        result_values[i], result_flags[i], previous_pos = _get_record(
            ts_index, ts_values, ts_flags, t, result_step, new_date_flag, previous_pos
        )


def _get_record(
    np.ndarray ts_index,
    np.ndarray ts_values,
    np.ndarray ts_flags,
    long t,
    long result_step,
    str new_date_flag,
    int previous_pos,
):
    cdef int i, found, count

    # Return the source record if it already exists
    found = False
    for i in range(previous_pos, ts_index.size):
        if ts_index[i] == t:
            found = True
            break
        if ts_index[i] > t:
            break
    if found:
        return ts_values[i], ts_flags[i], i

    # Otherwise get the nearby record, if it exists and is only one
    start = t - result_step / 2
    end = t + result_step / 2
    count = 0
    for i in range(previous_pos, ts_index.size):
        if ts_index[i] >= start and ts_index[i] < end:
            count += 1
        if ts_index[i] >= end:
            i -= 1
            break
    if count != 1:
        return np.nan, "", i
    value = ts_values[i]
    flags = ts_flags[i]
    if flags:
        flags += " "
    flags += "DATEINSERT"
    return value, flags, i + 1
