import time

# time.clock() returns the time since the method was first called, so if you
# want microsecond resolution wall time you could do something like this
# (https://stackoverflow.com/questions/1938048/high-precision-clock-in-python):
class Timer(object):
    def __init__(self):
        self._wall_time_0 = time.time()
        self._clock_0 = time.clock() if hasattr(time, 'clock') else None
        self._time = 0
        self._stopped = False

    def sample(self):
        if self._stopped: raise ValueError('Timer stopped')
        if self._clock_0 is not None:
            dc = time.clock() - self._clock_0  # @UndefinedVariable
            self._time = self._wall_time_0 + dc
        else:
            self._time = time.time() - self._wall_time_0
        return self._time
    
    def sample_and_stop(self):
        result = self.sample()
        self._stopped = True
        return result
    
    @property
    def stopped(self):
        return self._stopped
    
    @property
    def time(self):
        return self._time
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sample_and_stop()

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
