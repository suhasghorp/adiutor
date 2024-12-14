import unittest

import numpy.testing as npt

import thalesians.adiutor.number_theory as number_theory

class TestNumbers(unittest.TestCase):
    def test_features(self):
        features = number_theory.features(108)
        npt.assert_almost_equal(features['number'], 108)
        npt.assert_almost_equal(features['normalized_modulo_2'], 0.0)
        npt.assert_almost_equal(features['number_of_digits_2'], 7)
        npt.assert_almost_equal(features['centre_of_mass_2'], 2.0)
        npt.assert_almost_equal(features['normalized_centre_of_mass_2'], 0.2857142857142857)
        npt.assert_almost_equal(features['digits_mean_2'], 0.5714285714285714)
        npt.assert_almost_equal(features['digits_median_2'], 1.0)
        npt.assert_almost_equal(features['digits_std_2'], 0.4948716593053935)
        npt.assert_almost_equal(features['digits_skew_2'], -0.2886751345948128)
        npt.assert_almost_equal(features['digits_kurtosis_2'], -1.9166666666666665)
        npt.assert_almost_equal(features['normalized_modulo_3'], 0.0)
        npt.assert_almost_equal(features['number_of_digits_3'], 5)
        npt.assert_almost_equal(features['centre_of_mass_3'], 0.5)
        npt.assert_almost_equal(features['normalized_centre_of_mass_3'], 0.1)
        npt.assert_almost_equal(features['digits_mean_3'], 0.4)
        npt.assert_almost_equal(features['digits_median_3'], 0.0)
        npt.assert_almost_equal(features['digits_std_3'], 0.48989794855663565)
        npt.assert_almost_equal(features['digits_skew_3'], 0.4082482904638628)
        npt.assert_almost_equal(features['digits_kurtosis_3'], -1.8333333333333335)
        npt.assert_almost_equal(features['normalized_modulo_4'], 0.0)
        npt.assert_almost_equal(features['number_of_digits_4'], 4)
        npt.assert_almost_equal(features['centre_of_mass_4'], 1.0)
        npt.assert_almost_equal(features['normalized_centre_of_mass_4'], 0.25)
        npt.assert_almost_equal(features['digits_mean_4'], 1.5)
        npt.assert_almost_equal(features['digits_median_4'], 1.5)
        npt.assert_almost_equal(features['digits_std_4'], 1.118033988749895)
        npt.assert_almost_equal(features['digits_skew_4'], 0.0)
        npt.assert_almost_equal(features['digits_kurtosis_4'], -1.36)
        # ...
        npt.assert_almost_equal(features['normalized_modulo_30'], 0.6)
        npt.assert_almost_equal(features['number_of_digits_30'], 2)
        npt.assert_almost_equal(features['centre_of_mass_30'], 0.5)
        npt.assert_almost_equal(features['normalized_centre_of_mass_30'], 0.25)
        npt.assert_almost_equal(features['digits_mean_30'], 10.5)
        npt.assert_almost_equal(features['digits_median_30'], 10.5)
        npt.assert_almost_equal(features['digits_std_30'], 7.5)
        npt.assert_almost_equal(features['digits_skew_30'], 0.0)
        npt.assert_almost_equal(features['digits_kurtosis_30'], -2.0)

if __name__ == '__main__':
    unittest.main()
