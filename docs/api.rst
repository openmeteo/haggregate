===
API
===

``from haggregate import aggregate``


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
