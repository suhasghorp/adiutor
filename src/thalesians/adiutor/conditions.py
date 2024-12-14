# TODO Write a proper comment here
# Based on http://stackoverflow.com/questions/12151182/python-precondition-postcondition-for-member-function-how

import functools

from thalesians.adiutor.checks import check
import thalesians.adiutor.config as our_config

def conditions(pre=None, post=None, message='Condition violated', level=1):
    def decorator(func):
        # Use functools to preserve the name, docstring, etc.
        if our_config.MIN_PRECONDITION_LEVEL <= level and our_config.MIN_POSTCONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                if pre is not None:
                    check(pre(*args, **kwargs), message=lambda: message, level=level)
                retval = func(*args, **kwargs)
                if post is not None:
                    check(post(retval), message=lambda: message, level=level)
                return retval
        elif our_config.MIN_PRECONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                if pre is not None:
                    check(pre(*args, **kwargs), message=lambda: message, level=level)
                return func(*args, **kwargs)
        elif our_config.MIN_POSTCONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                retval = func(*args, **kwargs)
                if post is not None:
                    check(post(retval), message=lambda: message, level=level)
                return retval
        else:
            def wrapper(*args, **kwargs):  # NB: No self
                return func(*args, **kwargs)
        return wrapper
    return decorator

def precondition(check, message='Precondition violated', level=1):
    return conditions(pre=check, message=message, level=level)

def postcondition(check, message='Postcondition violated', level=1):
    return conditions(post=check, message=message, level=level)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
