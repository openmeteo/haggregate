===
API
===

.. function:: haggregate.regularize(ts, new_date_flag="DATEINSERT")

   Process *ts* (a HTimeseries_ object) and return a new time series
   (HTimeseries_ object), with a strict time step.

   The source time series, *ts*, must not be an irregular time series;
   it must have a time step, but this time step may have disturbances.
   For example, it may be a ten-minute time series like this::

       2008-02-07 10:10 10.54 
       2008-02-07 10:20 10.71 
       2008-02-07 10:41 10.93 
       2008-02-07 10:50 11.10 
       2008-02-07 11:00 11.23 

   The above has a missing record (10:30) and a disturbance in the time
   stamp of another record (10:41). :func:`regularize` would convert it
   to this::

       2008-02-07 10:10 10.54 
       2008-02-07 10:20 10.71 
       2008-02-07 10:30 empty
       2008-02-07 10:40 10.93
       2008-02-07 10:50 11.10 
       2008-02-07 11:00 11.23 

   That is, the result of :func:`regularize` is a time series with a
   regular time step from beginning to end, with no missing records.

   *ts* must have the ``time_step`` attribute set (see HTimeseries_).

   A **regular timestamp** is one that falls exactly on the round time
   step; e.g. for a ten-minute step, regular timestamps are 10:10,
   10:20, etc., whereas irregular timestamps are 10:11, 10:25, etc. For
   hourly time step, regular timestamps end in :00.

   The returned time series begins with the regular timestamp A which is
   nearest to the timestamp of the first record of *ts*, and ends at the
   timestamp B which is nearest to the last record of *ts*. Between A
   and B, the returned time series contains records for all regular
   timestamps, although some may be null.  The value and flags for each
   record with timestamp *t* are determined as follows:

   * If a record exists in *ts* and has timestamp *t*, that record's
     value and flags are used.
   * Otherwise, if a single not null record exists in *ts* such that its
     timestamp is between ``t - time_step/2`` (inclusive) and ``t +
     time_step/2`` (non-inclusive), then the value and flags of this
     record are used (plus *new_date_flag*, explained below).
   * Otherwise, the value is null and no flags are set.

   Whenever the algorithm results in creating a non-null record whose
   timestamp does not have an exact match in *ts*, the flag specified
   by *new_date_flag* is raised in the destination record, unless
   *new_date_flag* is the empty string.

   If an error occurs, such as *ts* not having the ``time_step``
   attribute, :exc:`RegularizeError` (or a sublcass) is raised.

   If you think the algorithm is insufficient and you intend to extend
   it with a more clever one that does interpolation, first check commit
   67bceaa, which had one (or the difference with the next commit).

.. function:: haggregate.aggregate(ts, target_step, method[, min_count=None][, missing_flag][, target_timestamp_offset])

   Process *ts* (a HTimeseries_ object) and return a new time series
   (HTimeseries_ object), with the aggregated series.  "target_step" and
   "target_timestamp_offset" are pandas "frequency" strings (see
   :ref:`usage` for more).  *method* is "sum", "mean", "max" or "min".
   *ts* must have a strictly regular step. If in doubt, call
   :func:`regularize` before calling :func:`aggregate`.

   If some of the source records corresponding to a destination record
   are missing, *min_count* specifies what will be done. If there fewer
   than *min_count* source records corresponding, the resulting
   destination record is null; otherwise, the destination record is
   derived even though some records are missing.  In that case, the flag
   specified by *missing_flag* is raised in the destination record.

   If an error occurs, such as *ts* not having a strictly regular step,
   :exc:`AggregateError` (or a subclass) is raised.

.. _HTimeseries: https://github.com/openmeteo/htimeseries
