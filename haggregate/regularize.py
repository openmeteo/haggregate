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
    index = pd.date_range(
        first_timestamp_of_result, last_timestamp_of_result, freq=freq
    )
    result.data = pd.DataFrame(index=index, columns=["value", "flags"]).fillna(
        value={"flags": ""}
    )

    # Calculate result.data
    result.data = result.data.apply(
        axis="columns", func=lambda x: _get_record(ts, x.name, step, new_date_flag)
    )

    return result


def _get_record(ts, current_timestamp, step, new_date_flag):
    # Return the source record if it already exists
    try:
        return ts.data.loc[current_timestamp]
    except KeyError:
        pass

    # Otherwise get the nearby record, if it exists and is only one
    start = current_timestamp - step / 2
    end = current_timestamp + step / 2
    timestamps = ts.data.index[ts.data.index >= start]
    timestamps = timestamps[timestamps < end]
    if len(timestamps) != 1:
        return pd.Series([None, ""], name=current_timestamp, index=["value", "flags"])
    value = ts.data.loc[timestamps[0]].value
    flags = ts.data.loc[timestamps[0]]["flags"]
    if flags:
        flags += " "
    flags += "DATEINSERT"
    return pd.Series([value, flags], name=current_timestamp, index=["value", "flags"])
