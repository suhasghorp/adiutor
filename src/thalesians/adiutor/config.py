import sys

# The __debug__ constant is True if Python was not started with an -O option.
if __debug__:  # @UndefinedVariable
    MIN_CHECK_LEVEL = 1
    MIN_PRECONDITION_LEVEL = 1
    MIN_POSTCONDITION_LEVEL = 1
else:
    MIN_CHECK_LEVEL = sys.maxsize
    MIN_PRECONDITION_LEVEL = sys.maxsize
    MIN_POSTCONDITION_LEVEL = sys.maxsize
