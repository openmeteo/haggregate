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
    if not hasattr(ts, "interval_type"):
        raise RegularizeError(
            "The source time series does not specify an interval type"
        )
    if ts.interval_type not in ("average", "sum"):
        raise RegularizeError(
            'The interval type "{}" is not supported. Only "average" and "sum" is '
            "supported.".format(ts.interval_type)
        )

    # Determine first and last timestamps
    freq = ts.time_step.split(",")[0].strip() + "min"
    step = pd.Timedelta(freq)
    first_timestamp_of_result = ts.data.index[0].round(step)
    last_timestamp_of_result = ts.data.index[-1].round(step)

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

    # Calculate result.data
    current_timestamp = first_timestamp_of_result
    while current_timestamp <= last_timestamp_of_result:
        result.data.loc[current_timestamp] = _get_record(
            ts, current_timestamp, step, new_date_flag
        )
        current_timestamp += step

    return result


def _get_record(ts, current_timestamp, step, new_date_flag):
    # Return the source record if it already exists
    try:
        return ts.data.loc[current_timestamp]
    except KeyError:
        pass

    if ts.interval_type == "average":
        return _calculate_inserted_record_for_average(
            ts, current_timestamp, step, new_date_flag
        )
    elif ts.interval_type == "sum":
        return _calculate_inserted_record_for_sum(
            ts, current_timestamp, step, new_date_flag
        )
    else:
        assert False


def _calculate_inserted_record_for_average(ts, current_timestamp, step, new_date_flag):
    # Find the first and the second source timestamp that we will use
    if current_timestamp < ts.data.index[0]:
        first_timestamp = ts.data.index[0]
        second_timestamp = ts.data.index[1]
    elif current_timestamp > ts.data.index[-1]:
        first_timestamp = ts.data.index[-2]
        second_timestamp = ts.data.index[-1]
    else:
        first_timestamp = ts.data.index[ts.data.index > current_timestamp][0]
        second_timestamp = ts.data.index[ts.data.index < current_timestamp][-1]

    # If any of the two source records is null, return null
    result_is_null = (
        ts.data.loc[first_timestamp].value is None
        or ts.data.loc[second_timestamp].value is None
    )
    if result_is_null:
        return {"value": None, "flags": ""}

    # If two source records aren't close enough to the current timestamp, return null
    diff_with_first = current_timestamp - first_timestamp
    diff_with_second = second_timestamp - current_timestamp
    if abs(diff_with_first) < abs(diff_with_second):
        small_diff = abs(diff_with_first)
        large_diff = abs(diff_with_second)
        nearest_timestamp = first_timestamp
    else:
        small_diff = abs(diff_with_second)
        large_diff = abs(diff_with_first)
        nearest_timestamp = second_timestamp
    if small_diff > 0.50 * step or large_diff > 1.50 * step:
        return {"value": None, "flags": ""}

    # Interpolate (or extrapolate) as needed (this may extrapolate for the first and
    # last record because diff_with_first or diff_with_second may be negative).
    total_diff = diff_with_second + diff_with_first
    value = ts.data.loc[second_timestamp].value * (
        diff_with_first / total_diff
    ) + ts.data.loc[first_timestamp].value * (diff_with_second / total_diff)
    old_flags = ts.data.loc[nearest_timestamp]["flags"]
    if old_flags:
        new_flags = old_flags + " " + new_date_flag
    else:
        new_flags = new_date_flag
    return {"value": value, "flags": new_flags}


def _calculate_inserted_record_for_sum(ts, current_timestamp, step, new_date_flag):
    start = current_timestamp - step / 2
    end = current_timestamp + step / 2
    timestamps = ts.data.index[ts.data.index >= start]
    timestamps = timestamps[timestamps < end]
    if len(timestamps) != 1:
        return {"value": None, "flags": ""}
    value = ts.data.loc[timestamps[0]].value
    flags = ts.data.loc[timestamps[0]]["flags"]
    if flags:
        flags += " "
    flags += "DATEINSERT"
    return {"value": value, "flags": flags}
