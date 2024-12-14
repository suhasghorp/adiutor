class NumericError(Exception):
    def __init__(self, message):
        super(NumericError, self).__init__(message)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
