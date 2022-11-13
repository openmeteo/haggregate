=======
History
=======

2.0.1 (2022-11-13)
==================

- Fixed inability to install with pip on Python 3.10 (no difference in
  code, it was only rebuilt in Python 3.10).

2.0.0 (2020-02-23)
==================

- Only Python>=3.7 is now supported.

1.0.2 (2020-01-22)
==================

- Fixed crash if result had only NaN values.

1.0.1 (2020-01-10)
==================

- Made installation process more robust. Sometimes it could fail,
  depending on the environment.

1.0.0 (2020-01-05)
==================

- Now uses version 5 of hts file (i.e. different time step notation).

0.2.0 (2019-12-05)
==================

- Added option target_timestamp_offset.

0.1.4 (2019-07-19)
==================

- Greatly reduced memory usage.

0.1.3 (2019-07-03)
==================

- Fixed bug where Timezone wasn't being set in the output file.

0.1.2 (2019-06-25)
==================

- Fixed erroneous setting of time_step, timestamp_rounding and
  timestamp_offset in the resulting time series.
- You can now import regularize from haggregate (before you imported it
  from haggregate.regularize).

0.1.1 (2019-06-24)
==================

- Initial release

  (There is also a 0.1.0 release on PyPI, which was uploaded during
  experimentation, but it doesn't work.)
