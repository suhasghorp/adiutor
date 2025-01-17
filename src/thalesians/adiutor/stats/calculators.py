"""
thalesians.adiutor.stats.calculators
====================================

This module implements a collection of incremental calculators for statistical computations. 
It is designed to support dynamic, streaming data analysis while minimizing memory usage. 
The calculators are highly extensible and cater to various statistical needs, including 
basic averages, moments, variances, covariances, and more advanced metrics like skewness, 
kurtosis, and quantiles.

Key Features
------------
1. **Incremental Calculators**:
   - Support for online computation of statistics without storing the entire dataset.
   - Efficient algorithms for streaming updates.

2. **Specialized Calculators**:
   - Central and standardized moments.
   - Geometric and harmonic means.
   - Variance, standard deviation, and covariance.
   - Quantiles, medians, and modes.

3. **Auto-Resetting and Window-Based Calculators**:
   - Auto-resetting calculators that adapt to changepoints in data streams.
   - Window-based calculators for rolling or fixed-size window statistics.

4. **Extensibility**:
   - Designed for easy integration with custom calculators and statistical methods.

Classes
-------
- **AbstractCalculator**:
  - Base class for all calculators, defining the structure and essential methods.
- **AbstractIncrementalCalculator**:
  - Base class for calculators that compute statistics incrementally.
- **AutoResettingIncrementalCalculator**:
  - Automatically resets calculations when a statistical changepoint is detected.
- **MomentIncrementalCalculator**:
  - Computes moments of any order.
- **CentralMomentIncrementalCalculator**:
  - Computes central moments (e.g., variance as the 2nd central moment).
- **StandardizedMomentIncrementalCalculator**:
  - Computes standardized moments (e.g., skewness, kurtosis).
- **ArithmeticMeanIncrementalCalculator**:
  - Calculates the arithmetic mean incrementally.
- **GeometricMeanIncrementalCalculator**:
  - Calculates the geometric mean incrementally.
- **HarmonicMeanIncrementalCalculator**:
  - Calculates the harmonic mean incrementally.
- **VarianceIncrementalCalculator**:
  - Calculates variance, optionally supporting semi-variance.
- **StandardDeviationIncrementalCalculator**:
  - Calculates the standard deviation based on variance.
- **CovarianceIncrementalCalculator**:
  - Calculates covariance incrementally for paired data.
- **ControlVariateIncrementalCalculator**:
  - Implements control variate adjustments for reducing variance.
- **WindowCalculator**:
  - Calculates statistics within a fixed or rolling window.

Functions
---------
- **make_skewness_calculator(window_size=None)**:
  - Creates a skewness calculator, optionally with a rolling window.
- **make_kurtosis_calculator(window_size=None)**:
  - Creates a kurtosis calculator, optionally with a rolling window.
- **make_quantile_calculator(quantile=0.5, window_size=None)**:
  - Creates a quantile calculator, optionally with a rolling window.
- **make_median_calculator(window_size=None)**:
  - Creates a median calculator, optionally with a rolling window.
- **make_mode_calculator(decimals=None, window_size=None)**:
  - Creates a mode calculator, optionally rounding to the specified decimal places.
- **make_median_absolute_deviation_calculator(window_size=None, power=1, factor=1.4826)**:
  - Creates a calculator for the median absolute deviation.

Dependencies
------------
- **NumPy**: For numerical computations and array operations.
- **SciPy**: For advanced statistical operations (e.g., mode calculation).
- **changepoint_online** (optional): For detecting changepoints in auto-resetting calculators.

Examples
--------
Basic Usage:
    >>> calc = ArithmeticMeanIncrementalCalculator()
    >>> calc.append(10)
    >>> calc.append(20)
    >>> calc.get_statistic()
    15.0

Auto-Resetting Calculator:
    >>> from changepoint_online import MDFocus, MDGaussian
    >>> changepoint_detector = MDFocus(MDGaussian())
    >>> calc = AutoResettingIncrementalCalculator(threshold=0.1, changepoint_detector=changepoint_detector)
    >>> for x in [10, 15, 20]:
    ...     calc.append(x)
    >>> calc.get_statistic()
    15.0

Rolling Window Median:
    >>> calc = make_median_calculator(window_size=3)
    >>> for x in [1, 2, 3, 4]:
    ...     calc.append(x)
    >>> calc.get_statistic()
    3.0

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import copy
import math

import numpy as np
import scipy.stats

class AbstractCalculator:
    def __init__(self):
        self._count = 0
        self._statistic = float('NaN')

    def get_count(self):
        return self._count

    def get_statistic(self):
        return self._statistic

    def append(self, x: float):
        raise NotImplementedError('Abstract method')

    def extend(self, xs):
        for x in xs: self.append(x)

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')

    def __repr__(self):
        s = self.__class__.__name__
        s += '('
        index = 0
        for key, value in self.__getstate__().items():
            if index > 0: s += ', '
            s += repr(key) + '=' + repr(value)
        s += ')'
        return s

    def __str__(self):
        s = self.__class__.__name__
        s += '('
        index = 0
        for key, value in self.__getstate__().items():
            if index > 0: s += ', '
            s += str(key) + '=' + str(value)
        s += ')'
        return s

class AbstractIncrementalCalculator(AbstractCalculator):
    def __init__(self):
        super().__init__()

class AutoResettingIncrementalCalculator(AbstractCalculator):
    def __init__(self, calculator=None, changepoint_detector=None, threshold=1.5e-5):
        import changepoint_online
        super().__init__()
        if changepoint_detector is None: changepoint_detector = changepoint_online.MDFocus(changepoint_online.MDGaussian(), pruning_params = (2, 1))
        if calculator is None: calculator = ArithmeticMeanIncrementalCalculator()
        self._calculator = calculator
        self._changepoint_detector_clone = copy.copy(changepoint_detector)
        self._changepoint_detector = copy.copy(self._changepoint_detector_clone)
        self._threshold = threshold
        self._last_auto_reset_count = None

    def get_statistic(self):
        return self._calculator.get_statistic()

    def append(self, x: float):
        self._count += 1
        self._changepoint_detector.update(x)
        if (self._last_auto_reset_count is None or self._count - self._last_auto_reset_count >= 10) and self._changepoint_detector.statistic() > self._threshold:
            print('!!! resetting', self._count)
            self._calculator.reset()
            self._last_auto_reset_count = self._count
        self._calculator.append(x)
        
    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._calculator.reset()
        self._changepoint_detector = copy.copy(self._changepoint_detector_clone)

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic,
            '_calculator': self._calculator,
            '_changepoint_detector': self._changepoint_detector,
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']
        self._calculator = state['_calculator']
        self._changepoint_detector = state['_changepoint_detector']

    def __reduce__(self):
        return (_create_auto_resetting_incremental_calculator, (), self.__getstate__())

def _create_auto_resetting_incremental_calculator():
    return AutoResettingIncrementalCalculator()

class MomentIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, n=1):
        super().__init__()
        self._n = n

    def append(self, x: float):
        self._statistic += (1. / (self._count + 1.)) * (np.power(x, self._n) - self._statistic)
        if isinstance(self._statistic, np.ndarray):
            self._statistic[self._statistic != self._statistic] = x[self._statistic != self._statistic]
        else:
            self._statistic = self._statistic if np.isfinite(self._statistic) else x
        self._count += 1

    def __getstate__(self):
        return {
            '_n': self._n,
            '_count': self._count,
            '_statistic': self._statistic,
        }

    def __setstate__(self, state):
        self._n = state['_n']
        self._count = state['_count']
        self._statistic = state['_statistic']

    def __reduce__(self):
        return (_create_moment_incremental_calculator, (), self.__getstate__())

def _create_moment_incremental_calculator():
    return MomentIncrementalCalculator()

class CentralMomentIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, n=1, inner_average_calculator=None, outer_average_calculator=None):
        super().__init__()
        self._n = n
        if inner_average_calculator is None: inner_average_calculator = ArithmeticMeanIncrementalCalculator()
        if outer_average_calculator is None: outer_average_calculator = ArithmeticMeanIncrementalCalculator()
        self._inner_average_calculator = inner_average_calculator
        self._outer_average_calculator = outer_average_calculator

    def get_statistic(self):
        return self._outer_average_calculator.get_statistic()

    def append(self, x: float):
        self._inner_average_calculator.append(x)
        self._outer_average_calculator.append(np.power(x - self._inner_average_calculator.get_statistic(), self._n))
        self._count += 1

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._inner_average_calculator.reset()
        self._outer_average_calculator.reset()

    def __getstate__(self):
        return {
            '_n': self._n,
            '_inner_average_calculator': self._inner_average_calculator,
            '_outer_average_calculator': self._outer_average_calculator,
            '_count': self._count,
            '_statistic': self._statistic
        }

    def __setstate__(self, state):
        self._n = state['_n']
        self._inner_average_calculator = state['_inner_average_calculator']
        self._outer_average_calculator = state['_outer_average_calculator']
        self._count = state['_count']
        self._statistic = state['_statistic']

    def __reduce__(self):
        return (_create_central_moment_incremental_calculator, (), self.__getstate__())

def _create_central_moment_incremental_calculator():
    return CentralMomentIncrementalCalculator()

class StandardizedMomentIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, n=1, inner_average_calculator=None, inner_standard_deviation_calculator=None, outer_average_calculator=None):
        super().__init__()
        self._n = n
        if inner_average_calculator is None: inner_average_calculator = ArithmeticMeanIncrementalCalculator()
        if inner_standard_deviation_calculator is None: inner_standard_deviation_calculator = StandardDeviationIncrementalCalculator()
        if outer_average_calculator is None: outer_average_calculator = ArithmeticMeanIncrementalCalculator()
        self._inner_average_calculator = inner_average_calculator
        self._inner_standard_deviation_calculator = inner_standard_deviation_calculator
        self._outer_average_calculator = outer_average_calculator

    def get_statistic(self):
        return self._outer_average_calculator.get_statistic()

    def append(self, x: float):
        self._inner_average_calculator.append(x)
        self._inner_standard_deviation_calculator.append(x)
        self._outer_average_calculator.append(np.power((x - self._inner_average_calculator.get_statistic() / self._inner_standard_deviation_calculator.get_statistic()), self._n))
        self._count += 1

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._inner_average_calculator.reset()
        self._inner_standard_deviation_calculator.reset()
        self._outer_average_calculator.reset()

    def __getstate__(self):
        return {
            '_n': self._n,
            '_inner_average_calculator': self._inner_average_calculator,
            '_inner_standard_deviation_calculator': self._inner_standard_deviation_calculator,
            '_outer_average_calculator': self._outer_average_calculator,
            '_count': self._count,
            '_statistic': self._statistic
        }

    def __setstate__(self, state):
        self._n = state['_n']
        self._inner_average_calculator = state['_inner_average_calculator']
        self._inner_standard_deviation_calculator = state['_inner_standard_deviation_calculator']
        self._outer_average_calculator = state['_outer_average_calculator']
        self._count = state['_count']
        self._statistic = state['_statistic']

    def __reduce__(self):
        return (_create_standardized_moment_incremental_calculator, (), self.__getstate__())

def _create_standardized_moment_incremental_calculator():
    return StandardizedMomentIncrementalCalculator()

class ArithmeticMeanIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self):
        super().__init__()

    def append(self, x: float):
        self._statistic += (1. / (self._count + 1.)) * (x - self._statistic)
        if isinstance(self._statistic, np.ndarray):
            self._statistic[self._statistic != self._statistic] = x[self._statistic != self._statistic]
        else:
            self._statistic = self._statistic if np.isfinite(self._statistic) else x
        self._count += 1

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']

    def __reduce__(self):
        return (_create_arithmetic_mean_incremental_calculator, (), self.__getstate__())

def _create_arithmetic_mean_incremental_calculator():
    return ArithmeticMeanIncrementalCalculator()

class GeometricMeanIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, return_radius=True):
        super().__init__()
        self._count_of_negatives = 0
        self._return_radius = return_radius

    def append(self, x: float):
        if math.isnan(self._statistic):
            self._statistic = np.log(np.abs(x))
        else:
            self._statistic += (1. / (self._count + 1.)) * (np.log(np.abs(x)) - self._statistic)
        self._count += 1
        if x < 0.: self._count_of_negatives += 1

    def get_statistic(self):
        statistic = np.power(np.power(np.asarray(-1., dtype=complex), self._count_of_negatives), 1. / self._count) * np.exp(self._statistic)
        if self._return_radius: statistic = abs(statistic)
        return statistic

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._count_of_negatives = 0

class HarmonicMeanIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, average_calculator=None):
        super().__init__()
        if average_calculator is None: average_calculator = ArithmeticMeanIncrementalCalculator()
        self._ac = average_calculator

    def append(self, x: float):
        self._ac.append(1. / x)

    def get_statistic(self):
        return 1. / self._ac.get_statistic()

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._ac.reset()

class AverageAbsoluteDeviationIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, inner_average_calculator=None, outer_average_calculator=None):
        super().__init__()
        if inner_average_calculator is None: inner_average_calculator = ArithmeticMeanIncrementalCalculator()
        self._inner_average_calculator = inner_average_calculator
        if outer_average_calculator is None: outer_average_calculator = ArithmeticMeanIncrementalCalculator()
        self._outer_average_calculator = outer_average_calculator

    def append(self, x: float):
        self._inner_average_calculator.append(x)
        absolute_difference = np.abs(x - self._inner_average_calculator.get_statistic())
        self._outer_average_calculator.append(absolute_difference)
        self._count += 1

    def get_statistic(self):
        return self._outer_average_calculator.get_statistic()

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._inner_average_calculator.reset()
        self._outer_average_calculator.reset()

class VarianceIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, ddof=1, semi=False, average_calculator=None):
        super().__init__()
        if average_calculator is None: average_calculator = ArithmeticMeanIncrementalCalculator()
        self._average_calculator = average_calculator
        self._ddof = ddof
        self._semi = semi

    def append(self, x: float):
        self._count += 1
        delta = x - self._average_calculator.get_statistic() if self._count > 1 else 0.
        self._average_calculator.append(x)
        delta2 = x - self._average_calculator.get_statistic()
        if self._semi: delta2 = np.minimum(delta2, 0.)
        product = delta * delta2
        self._statistic += product
        if isinstance(self._statistic, np.ndarray):
            self._statistic[self._statistic != self._statistic] = product[self._statistic != self._statistic]
        else:
            self._statistic = self._statistic if np.isfinite(self._statistic) else product

    def get_statistic(self):
        if self._count < 2: return np.nan
        return self._statistic / (self._count - self._ddof)

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._average_calculator.reset()

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic,
            '_average_calculator': self._average_calculator,
            '_ddof': self._ddof
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']
        self._average_calculator = state['_average_calculator']
        self._ddof = state['_ddof']

    def __reduce__(self):
        return (_create_variance_incremental_calculator, (), self.__getstate__())

def _create_variance_incremental_calculator():
    return VarianceIncrementalCalculator()

class StandardDeviationIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, variance_calculator=None):
        super().__init__()
        if variance_calculator is None: variance_calculator = VarianceIncrementalCalculator(ddof=1.5)
        self._variance_calculator = variance_calculator

    def append(self, x: float):
        self._count += 1
        self._variance_calculator.append(x)

    def get_statistic(self):
        return np.sqrt(self._variance_calculator.get_statistic())

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._variance_calculator.reset()

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic,
            '_variance_calculator': self._variance_calculator
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']
        self._variance_calculator = state['_variance_calculator']

    def __reduce__(self):
        return (_create_standard_deviation_incremental_calculator, (), self.__getstate__())

def _create_standard_deviation_incremental_calculator():
    return StandardDeviationIncrementalCalculator()

class CovarianceIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, ddof=1, average_calculator1=None, average_calculator2=None):
        super().__init__()
        if average_calculator1 is None: average_calculator1 = ArithmeticMeanIncrementalCalculator()
        self._average_calculator1 = average_calculator1
        if average_calculator2 is None: average_calculator2 = ArithmeticMeanIncrementalCalculator()
        self._average_calculator2 = average_calculator2
        self._ddof = ddof

    def append(self, x):
        self._count += 1
        delta1 = x[0] - self._average_calculator1.get_statistic()
        self._average_calculator1.append(x[0])
        self._average_calculator2.append(x[1])
        delta2 = x[1] - self._average_calculator2.get_statistic()
        if math.isnan(self._statistic):
            self._statistic = delta1 * delta2
        else:
            self._statistic += delta1 * delta2

    def get_statistic(self):
        if self._count < 2: return np.nan
        return self._statistic / float(self._count - self._ddof)

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._average_calculator1.reset()
        self._average_calculator2.reset()

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic,
            '_average_calculator1': self._average_calculator1,
            '_average_calculator2': self._average_calculator2
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']
        self._average_calculator1 = state['_average_calculator1']
        self._average_calculator2 = state['_average_calculator2']

    def __reduce__(self):
        return (_create_covariance_incremental_calculator, (), self.__getstate__())

def _create_covariance_incremental_calculator():
    return CovarianceIncrementalCalculator()

class ControlVariateIncrementalCalculator(AbstractIncrementalCalculator):
    def __init__(self, calculator, control_variate_calculator=None, control_variate_mean_calculator=None, control_variate_variance_calculator=None, covariance_calculator=None):
        super().__init__()
        self._calculator = calculator
        self._control_variate_calculator = control_variate_calculator
        if control_variate_mean_calculator is None: control_variate_mean_calculator = ArithmeticMeanIncrementalCalculator()
        self._control_variate_mean_calculator = control_variate_mean_calculator
        if control_variate_variance_calculator is None: control_variate_variance_calculator = VarianceIncrementalCalculator()
        self._control_variate_variance_calculator = control_variate_variance_calculator
        if covariance_calculator is None: covariance_calculator = CovarianceIncrementalCalculator()
        self._covariance_calculator = covariance_calculator

    def append(self, x: float, control_variate=None):
        if control_variate is None:
            self._control_variate_calculator.append(x)
            control_variate = self._control_variate_calculator.get_statistic()
        y = control_variate
        self._control_variate_mean_calculator.append(y)
        control_variate_mean = self._control_variate_mean_calculator.get_statistic()
        self._control_variate_variance_calculator.append(y)
        control_variate_variance = self._control_variate_variance_calculator.get_statistic()
        self._covariance_calculator.append((x, y))
        covariance = self._covariance_calculator.get_statistic()
        modified_x = x - (covariance / control_variate_variance) * (y - control_variate_mean)
        if not np.isfinite(modified_x): modified_x = x
        self._calculator.append(modified_x)
        self._count += 1

    def get_statistic(self):
        return self._calculator.get_statistic()

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        self._calculator.reset()
        if self._control_variate_calculator is not None: self._control_variate_calculator.reset()
        self._control_variate_mean_calculator.reset()
        self._control_variate_variance.calculator.reset()
        self._covariance_calculator.reset()

class WindowCalculator(AbstractCalculator):
    def __init__(self, calculator=None, function=None, window_size=None):
        super().__init__()
        assert (calculator is not None) or (function is not None)
        self._calculator = calculator
        self._function = function
        self._window_size = window_size
        self._window = []

    def append(self, x: float):
        self._count += 1
        self._window.append(x)
        while self._window_size is not None and len(self._window) > self._window_size:
            self._window.pop(0)
        if self._calculator is not None:
            self._calculator.reset()
            self._calculator.extend(self._window)

    def get_statistic(self):
        if self._calculator is not None:
            result = self._calculator.get_statistic()
        else:
            result = self._function(self._window)
        return result

    def reset(self):
        self._count = 0
        self._statistic = float('NaN')
        if self._calculator is not None: self._calculator.reset()
        self._window.clear()

    def __getstate__(self):
        return {
            '_count': self._count,
            '_statistic': self._statistic,
            '_window_size': self._window_size,
            '_window': list(self._window),
            '_calculator': self._calculator,
            '_function': self._function,
        }

    def __setstate__(self, state):
        self._count = state['_count']
        self._statistic = state['_statistic']
        self._window_size = state['_window_size']
        self._window.clear()
        for x in state['_window']: self._window.push_back(x)
        self._calculator = state['_calculator']
        self._function = state['_function']

    def __reduce__(self):
        return (_create_window_calculator, (), self.__getstate__())

def _create_window_calculator():
    return WindowCalculator(calculator=ArithmeticMeanIncrementalCalculator(), window_size=10)

def make_skewness_calculator(window_size=None):
    calculator = StandardizedMomentIncrementalCalculator(n=3)
    if window_size is not None: calculator = WindowCalculator(calculator=calculator, window_size=window_size)
    return calculator

def make_kurtosis_calculator(window_size=None):
    calculator = StandardizedMomentIncrementalCalculator(n=4)
    if window_size is not None: calculator = WindowCalculator(calculator=calculator, window_size=window_size)
    return calculator

def make_quantile_calculator(quantile=.5, window_size=None):
    return WindowCalculator(function=lambda xs: np.quantile(xs, .5) if len(xs) > 0 else np.nan, window_size=window_size)

def make_median_calculator(window_size=None):
    return make_quantile_calculator(quantile=.5, window_size=window_size)

def make_mode_calculator(decimals=None, window_size=None):
    if decimals is None:
        return WindowCalculator(calculator=None, function=lambda xs: scipy.stats.mode(xs).mode, window_size=window_size)
    else:
        return WindowCalculator(calculator=None, function=lambda xs: scipy.stats.mode([np.round(x, decimals=decimals) for x in xs]).mode, window_size=window_size)

def make_median_absolute_deviation_calculator(window_size=None, power=1, factor=1.4826):
    return WindowCalculator(function=lambda xs: np.power((np.quantile(np.abs(xs - np.quantile(xs, .5)), .5) if len(xs) > 0 else np.nan) * factor, power), window_size=window_size)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
