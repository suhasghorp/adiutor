from IPython.core.magic import register_line_magic
from IPython.lib import backgroundjobs as bg

@register_line_magic
def start(fun):
    jobs = bg.BackgroundJobManager()
    jobs.new(fun)
    return jobs

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
