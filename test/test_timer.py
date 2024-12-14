import time
import unittest

import thalesians.adiutor.timer as timer

class TestTimer(unittest.TestCase):
    def test_timer(self):
        with timer.Timer() as t:
            time.sleep(5.)
        self.assertTrue(t.stopped)
        self.assertGreater(t.time, 4.)
        self.assertLess(t.time, 6.)

if __name__ == '__main__':
    unittest.main()
