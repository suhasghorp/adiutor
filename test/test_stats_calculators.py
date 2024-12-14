import unittest

import numpy as np
import numpy.testing as npt
import pandas as pd
import scipy.stats.mstats

import thalesians.adiutor.stats.calculators as our_calculators

class TestBasicStatistics(unittest.TestCase):
    def setUp(self):
        self.data_1 = [.34, .65, .21, .43, .23, .23, .12, .54, .98, .32]
        self.data_2 = [.78, .90, .32, .32, .32, .12, .65, .90, .09, .10]
    
    def test_arithmetic_mean_incremental_calculator(self):
        calculator = our_calculators.ArithmeticMeanIncrementalCalculator()
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = np.mean(self.data_1)
        npt.assert_almost_equal(actual, expected)

    def test_geometric_mean_incremental_calculator(self):
        calculator = our_calculators.GeometricMeanIncrementalCalculator()
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = scipy.stats.mstats.gmean(self.data_1)
        npt.assert_almost_equal(actual, expected)

    def test_harmonic_mean_incremental_calculator(self):
        calculator = our_calculators.HarmonicMeanIncrementalCalculator()
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = scipy.stats.mstats.hmean(self.data_1)
        npt.assert_almost_equal(actual, expected)

    def test_mean_absolute_deviation_incremental_calculator(self):
        calculator = our_calculators.AverageAbsoluteDeviationIncrementalCalculator()
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = np.mean(np.abs(self.data_1 - np.cumsum(self.data_1) / range(1, len(self.data_1) + 1)))
        npt.assert_almost_equal(actual, expected)

    def test_median_absolute_deviation_incremental_calculator(self):
        inner_average_calculator = our_calculators.make_median_calculator()
        calculator = our_calculators.AverageAbsoluteDeviationIncrementalCalculator(inner_average_calculator=inner_average_calculator)
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = np.mean(np.abs(self.data_1 - pd.Series(self.data_1).expanding().median().values))
        npt.assert_almost_equal(actual, expected)

    def test_variance_incremental_calculator(self):
        calculator = our_calculators.VarianceIncrementalCalculator()
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = np.var(self.data_1, ddof=1)
        npt.assert_almost_equal(actual, expected)

    def test_covariance_incremental_calculator(self):
        calculator = our_calculators.CovarianceIncrementalCalculator(ddof=1)
        for datum_1, datum_2 in zip(self.data_1, self.data_2):
            calculator.append((datum_1, datum_2))
        actual = calculator.get_statistic()
        expected = np.cov(self.data_1, self.data_2, rowvar=False, ddof=1)[0, 1]
        npt.assert_almost_equal(actual, expected)

    def test_window_calculator(self):
        window_size = 3
        calculator = our_calculators.WindowCalculator(our_calculators.ArithmeticMeanIncrementalCalculator(), window_size=window_size)
        for datum in self.data_1:
            calculator.append(datum)
        actual = calculator.get_statistic()
        expected = np.mean(self.data_1[-window_size:])
        npt.assert_almost_equal(actual, expected)

if __name__ == '__main__':
    unittest.main()
