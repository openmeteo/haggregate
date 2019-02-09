=====
Usage
=====

Synopsis
========

``haggregate [--traceback] config_file``

Description and quick start
===========================

``haggregate`` gets the data of time series from files and creates time
series of a larger time step, storing the result in files.  The
details of its operation are specified in the configuration file
specified on the command line.

Installation
------------

``pip install haggregate``

How to run it
-------------

First, you need to create a configuration file with a text editor such
as ``vim``, ``emacs``, ``notepad``, or whatever. Create such a file
and name it, for example, :file:`/var/tmp/aggregate.conf`, or, on
Windows, something like :file:`C:\\Users\\user\\aggregate.conf`, with
the following contents (the contents don't matter at this stage, just
copy and paste them from below)::

    [General]
    loglevel = INFO

Then, open a command prompt and give it this command:

**Unix/Linux**::

    aggregate /var/tmp/aggregate.conf

**Windows**::

    C:\Program Files\Pthelma\aggregate.exe C:\Users\user\aggregate.conf

(the details may differ; for example, in 64-bit Windows, it may be
:file:`C:\\Program Files (x86)` instead of :file:`C:\\Program Files`.)

If you have done everything correctly, it should output an error message
complaining that something in its configuration file isn't right.

Configuration file example
--------------------------

Take a look at the following example configuration file and read the
explanatory comments that follow it:

.. code-block:: ini

    [General]
    loglevel = INFO
    logfile = C:\Somewhere\aggregate.log
    base_dir = C:\Somewhere
    target_step = 60,0

    [temperature]
    source_file = temperature-10min.hts
    target_file = temperature-hourly.hts
    interval_type = average

    [rainfall]
    source_file = rainfall-10min.hts
    target_file = rainfall-hourly.hts
    interval_type = sum

With the above configuration file, ``aggregate`` will log information in
the file specified by :option:`logfile`. It will aggregate the
specified time series into hourly (60 minutes, 0 months). The
filenames specified with :option:`source_file` and
:option:`target_file` are relative to :option:`base_dir`. For the
temperature, source records will be averaged, whereas for rainfall
they will be summed.

Configuration file reference
============================

The configuration file has the format of INI files. There is a
``[General]`` section with general parameters, and any number of other
sections, which we will call "time series sections", each time series
section referring to one time series.

General parameters
------------------

.. option:: loglevel

   Optional. Can have the values ``ERROR``, ``WARNING``, ``INFO``,
   ``DEBUG``.  The default is ``WARNING``.

.. option:: logfile

   Optional. The full pathname of a log file. If unspecified, log
   messages will go to the standard error.

.. option:: base_dir

   Optional. ``aggregate`` will change directory to this directory, so
   any relative filenames will be relative to this directory. If
   unspecified, relative filenames will be relative to the directory
   from which ``aggregate`` was started.

.. option:: target_step

   A string specifying the target time step, as a pandas "frequency".
   Examples of steps are "D" for day, "H" for hour, "T" or "min" for
   minute, "M" for month end, "MS" for month begin, "A-SEP" for year
   anchored 30 September, "AS_OCT" for year anchored 1 October. You can
   also use multipliers, like "30T" for 30 minutes.

.. option:: min_count
            missing_flag

   If some of the source records corresponding to a destination record
   are missing, :option:`min_count` specifies what will be done. If
   there are fewer than :option:`min_count` source records corresponding
   to a destination record, the resulting destination record is null;
   otherwise, the destination record is derived even though some records
   are missing. In that case, the flag specified by
   :option:`missing_flag` is raised in the destination record.

Time series sections
--------------------

The name of the section is ignored.

.. option:: source_file

   The filename of the source file with the time series, in `file
   format`_; it must be absolute or relative to :option:`base_dir`.

.. option:: target_file

   The filename of the target file, which will be written in `file
   format`_; it must be absolute or relative to :option:`base_dir`. In
   this version of ``haggregate``, all the aggregation is repeated even
   if it or part of it has been done in the past, and the file is
   entirely overwritten if it already exists.

.. option:: method

   How the aggregation will be performed; one of "mean", "sum",
   "max" and "min".

.. _file format: https://github.com/openmeteo/htimeseries/#file-format