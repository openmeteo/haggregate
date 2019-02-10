===
API
===

``from haggregate import aggregate, regularize``

.. function:: regularize(ts, new_date_flag="DATEINSERT")

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
       2008-02-07 10:40 10.91
       2008-02-07 10:50 11.10 
       2008-02-07 11:00 11.23 

   (The exact value assigned to 10:40 depends on details explained
   below.)

   That is, the result of :func:`regularize` is a time series with a
   regular time step from beginning to end, with no missing records.

   *ts* must have the ``time_step`` and ``interval_type`` attributes
   set (see HTimeseries_), and :func:`regularize` uses them to determine
   exactly how to perform the regularization.

   A **regular timestamp** is one that falls exactly on the round time
   step; e.g. for a ten-minute step, regular timestamps are 10:10,
   10:20, etc., whereas irregular timestamps are 10:11, 10:25, etc. For
   hourly time step, regular timestamps end in :00.

   The returned time series begins with the regular timestamp A which is
   nearest to the timestamp of the first record of *ts*, and ends at
   the timestamp B which is nearest to the last record of *ts*. Between
   A and B, the returned time series contains records for all regular
   timestamps, although some may be null.

   The algorithm depends on ``ts.interval_type``. Currently only
   "average" and "sum" is supported for the interval_type. In addition,
   for sum, it is always assumed that each record in *ts* contains a
   measurement which lasted for the specified time step, regardless of
   the time elpsed from the previous measurement.  (If you need to
   extend the algorithm for more cases besides "average" and "sum",
   :file:`tsprocess.pas` of Thelma already has other cases, including
   offsets from the round timestamp and a version of "sum" that means a
   measurement that began on the timestamp of the previous record.)

   For "average", the value and flags for each record with timestamp
   *t* are determined as follows:

   * If a record exists in *ts* and has timestamp *t*, that record's
     value and flags are used.
   * Otherwise, if two successive not null records exist in *ts* such
     that *t* is between their timestamps, and the time difference
     between the resulting record and the two source records is no more
     than ``0.50 * time_step`` for the one and ``1.50 * time_step`` for
     the other, then the value is found by interpolating between the
     two records, and the flags of the source record closest to the
     resulting record are used (plus *new_date_flag*, explained below).
   * Likewise for the first record of the result, but with
     extrapolation, provided that *t* is less than the first record of
     *ts*, but by no more than ``0.50 * time_step``, and no more than
     ``1.50 * time_step`` from the second record.
   * Likewise for the last record.
   * Otherwise, the value is null and no flags are set.

   For "sum", the value and flags for each record with timestamp *t*
   are determined as follows:

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

   If an error occurs, such as *ts* not having appropriate attributes,
   :exc:`RegularizeError` (or a sublcass) is raised.

.. function:: aggregate(ts, target_step, method[, min_count=None][, missing_flag])

   Process *ts* (a HTimeseries_ object) and return a new time series
   (HTimeseries_ object), with the aggregated series.  "target_step" is
   a pandas "frequency" string.  *method* is "sum", "mean", "max" or
   "min".

   If some of the source records corresponding to a destination record
   are missing, *min_count* specifies what will be done. If there fewer
   than *min_count* source records corresponding, the resulting
   destination record is null; otherwise, the destination record is
   derived even though some records are missing.  In that case, the flag
   specified by *missing_flag* is raised in the destination record.

.. _HTimeseries: https://github.com/openmeteo/htimeseries
