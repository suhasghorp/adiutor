import unittest
import datetime as dt

import numpy as np
import numpy.testing as npt

import thalesians.adiutor.exceptions as exc
import thalesians.adiutor.randomness as rnd

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers)

class TestRandom(unittest.TestCase):
    def test_random_state(self):
        rs = np.random.RandomState(seed=42)
        rnd.random_state(rs, force=True)
        self.assertEqual(rnd.random_state(), rs)
        with self.assertRaises(exc.NumericError):
            rnd.random_state(rs)
        rs = np.random.RandomState(seed=132)
        rnd.random_state(rs, force=True)
        self.assertEqual(rnd.random_state(), rs)
            
    def test_exponential(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        values = rnd.exponential(.25, size=5)
        npt.assert_almost_equal(values, np.array([ 0.117317 ,  0.7525304,  0.3291864,  0.2282356,  0.0424062]))
        
        values = rnd.exponential(.25, size=1000000)
        npt.assert_almost_equal(np.mean(values), .25, decimal=3)
        
        values = rnd.exponential(dt.timedelta(minutes=25), size=5)
        values = [v.total_seconds() for v in values]
        npt.assert_almost_equal(values, np.array([1138.023383, 2274.520394, 265.023984, 221.528354, 3365.675561]))
        
        values = rnd.exponential(dt.timedelta(minutes=25), size=1000000)
        npt.assert_almost_equal(np.mean([v.total_seconds() for v in values]), 1497.6779794581771, decimal=3)
        
if __name__ == '__main__':
    unittest.main()
    