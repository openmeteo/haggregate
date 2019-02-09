import textwrap
from io import StringIO
from unittest import TestCase

import pandas as pd
from htimeseries import HTimeseries

from haggregate import aggregate


tenmin_test_timeseries = textwrap.dedent(
    """\
            2008-02-07 09:40,10.32,
            2008-02-07 09:50,10.42,
            2008-02-07 10:00,10.51,
            2008-02-07 10:10,10.54,
            2008-02-07 10:20,10.71,
            2008-02-07 10:30,10.96,
            2008-02-07 10:40,10.93,
            2008-02-07 10:50,11.10,
            2008-02-07 11:00,11.23,
            2008-02-07 11:10,11.44,
            2008-02-07 11:20,11.41,
            2008-02-07 11:30,11.42,MISS
            2008-02-07 11:40,11.54,
            2008-02-07 11:50,11.68,
            2008-02-07 12:00,11.80,
            2008-02-07 12:10,11.91,
            2008-02-07 12:20,12.16,
            2008-02-07 12:30,12.16,
            2008-02-07 12:40,12.24,
            2008-02-07 12:50,12.13,
            2008-02-07 13:00,12.17,
            2008-02-07 13:10,12.31,
            """
)


tenmin_allmiss_test_timeseries = textwrap.dedent(
    """\
            2005-05-01 00:10,,
            2005-05-01 00:20,,
            2005-05-01 00:30,,
            2005-05-01 00:40,,
            2005-05-01 00:50,,
            2005-05-01 01:00,,
            2005-05-01 01:10,,
            2005-05-01 01:20,1,
            2005-05-01 01:30,,
            2005-05-01 01:40,1,
            2005-05-01 01:50,,
            2005-05-01 02:00,1,
            """
)


aggregated_hourly_allmiss = textwrap.dedent(
    """\
            2005-05-01 02:00,3,MISS\r
            """
)


class HourlySumTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "H", "sum", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 31.25)
        self.assertEqual(self.result.data["flags"].loc["2008-02-07 10:00"], "MISS")

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 65.47)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 69.29)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 72.77)


class HourlySumWithLargerMinCountTestCase(TestCase):
    """Same as HourlySumTestCase but with slightly larger min_count.
    """

    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "H", "sum", min_count=4, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 3)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 65.47)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 69.29)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 72.77)


class HourlyMeanTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "H", "mean", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 10:00"].value, 10.4166667
        )

    def test_value_2(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 11:00"].value, 10.9116667
        )

    def test_value_3(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 12:00"].value, 11.5483333
        )

    def test_value_4(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 13:00"].value, 12.1283333
        )


class HourlyMaxTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "H", "max", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 10.51)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 11.23)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 11.8)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 12.24)


class HourlyMinTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "H", "min", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 10.32)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 10.54)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 11.41)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 11.91)


class AggregateEmptyTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries()
        self.result = aggregate(self.ts, "H", "sum", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 0)


class AllMissAggregateTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries.read(StringIO(tenmin_allmiss_test_timeseries))
        self.result = aggregate(self.ts, "H", "sum", min_count=1, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 1)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2005-05-01 02:00"].value, 3)