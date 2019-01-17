===
API
===

``from haggregate import aggregate``



.. function:: aggregate(ts, target_step[, missing_allowed=0.0][, missing_flag][, last_incomplete=False][, all_incomplete=False])

   Process *ts* (a Htimeseries_ the `ts`time series, produce two new time series, and return
   these new time series as a tuple.  The first of these series is
   the aggregated series; the second one is the number of missing
   values in each time step (more on this below). Both produced
   time series have a time step of *target_step*, which must be a
   :class:`TimeStep` object.  The *timestamp_rounding*,
   *timestamp_offset*, and *interval_type* attributes of
   *target_step* are taken into account during aggregation; so if,
   for example, *target_step* is one day with
   ``timestamp_rounding=(480,0)``, ``timestamp_offset=(0,0)``, and
   an *interval_type* of ``IntervalType.SUM``, then aggregation is
   performed so that, in the resulting time series, a record with
   timestamp 2008-01-17 08:00 contains the sum of the values of the
   source series from 2008-01-16 08:00 to 2008-01-17 08:00.

   If *target_step.interval_type* is ``IntervalType.VECTOR_AVERAGE``,
   then the source records are considered to be directions in degrees
   (as in a wind direction time series); each produced record is the
   direction in degrees of the sum of the unit vectors whose direction
   is specified by the source records.

   If *target_step.interval_type* is ``None``, corresponding to
   instantaneous values, then for each record of the destination
   series, a record from the source time series is selected if this
   has the same nominal step. If a record is not found, then the
   resulting record is set as NULL.

   If some of the source records corresponding to a destination record
   are missing, *missing_allowed* specifies what will be done. If the
   ratio of missing values to existing values in the source record is
   greater than *missing_allowed*, the resulting destination record is
   null; otherwise, the destination record is derived even though some
   records are missing.  In that case, the flag specified by
   *missing_flag* is raised in the destination record. The second time
   series returned in the return tuple contains, for each destination
   record, a record with the same date, containing the number of
   missing source values for that destination record.

   If *last_incomplete* set to True, then the last record
   of the destination time series, can be derived from an
   incomplete month, year etc. If *all_incomplete* is set to True,
   then all the destination records are from aggregation to the
   same point as the last incomplete record. This is usefull to
   find i.e. the rainfall up to the same day for the year, when
   that day is the last daily record to be aggregated.
