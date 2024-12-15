"""
thalesians.adiutor.stats
========================

This module provides tools and utilities for statistical computations, focusing on covariance, correlation, and volatility 
matrix operations, as well as online statistical calculations. The functions and classes are designed to be efficient, 
robust, and flexible, catering to applications in quantitative finance, risk modeling, and data analysis.

Key Features
------------
1. **Covariance and Volatility Matrix Operations**:
    - Create covariance matrices from standard deviations and correlations.
    - Convert correlation matrices to covariance matrices.
    - Compute Cholesky decompositions and volatility matrices.

2. **Online Statistics Calculator**:
    - Incrementally compute statistics (mean, variance, standard deviation, etc.) for streaming data.
    - Designed for dynamic updates without storing the entire dataset.

3. **Utility Integrations**:
    - Leverages utilities from `thalesians.adiutor.numpy_utils` and `thalesians.adiutor.utils` for robust matrix handling.

Functions
---------
- `make_cov_2d(sd1, sd2, cor)`: Constructs a 2D covariance matrix from standard deviations and correlation.
- `make_vol_2d(sd1, sd2, cor)`: Constructs a 2D volatility matrix (Cholesky-like decomposition).
- `cov_to_vol(cov)`: Converts a covariance matrix to its Cholesky decomposition or element-wise square root.
- `cor_to_cov(cors, vars=None, sds=None, copy=True)`: Converts a correlation matrix to a covariance matrix.
- `vol_to_cov(vol)`: Computes a covariance matrix from a volatility matrix.
- `cholesky_sqrt_2d(sd1, sd2, cor)`: Creates a 2D Cholesky-like decomposition matrix.

Classes
-------
- `OnlineStatsCalculator`: A class for online computation of summary statistics. 
    - Properties include: `mean`, `variance`, `standard deviation`, `RMS`, and more.
    - Methods: `add(x)`, `add_all(xs)`, `reset(zero)`.

Testing
-------
- The module includes a `_test()` function that uses Python's `doctest` module for validating functionality.

Dependencies
------------
- `numpy`: For numerical computations.
- `thalesians.adiutor.numpy_utils`: Provides utility functions for handling matrices.
- `thalesians.adiutor.utils`: Includes specialized utilities for handling custom array types like `DiagonalArray` and `SubdiagonalArray`.

Examples
--------
Creating a covariance matrix from standard deviations and correlation:
    >>> make_cov_2d(0.2, 0.3, 0.5)
    array([[0.04 , 0.03 ],
           [0.03 , 0.09 ]])

Using the `OnlineStatsCalculator` for streaming updates:
    >>> calc = OnlineStatsCalculator()
    >>> calc.add(10)
    >>> calc.add(20)
    >>> calc.mean
    15.0
    >>> calc.var
    50.0

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import numpy as np

import thalesians.adiutor.numpy_utils as npu
import thalesians.adiutor.utils as utils

def make_cov_2d(sd1, sd2, cor):
    offdiag = cor*sd1*sd2
    return np.array([[sd1*sd1, offdiag], [offdiag, sd2*sd2]])

def make_vol_2d(sd1, sd2, cor):
    return np.array([[sd1, 0.], [cor*sd2, np.sqrt(1. - cor*cor)*sd2]])

def cov_to_vol(cov):
    cov = npu.to_ndim_2(cov, ndim_1_to_col=True, copy=False)
    return np.asarray(np.sqrt(cov)) if (np.isscalar(cov) or np.size(cov) == 1) else np.linalg.cholesky(cov)
    
def cor_to_cov(cors, vars=None, sds=None, copy=True):  # @ReservedAssignment
    assert (vars is None and sds is not None) or (vars is not None and sds is None)
    sds = np.sqrt(vars) if vars is not None else sds
    if isinstance(cors, (utils.DiagonalArray, utils.SubdiagonalArray)):
        cors = cors.to_numpy_array()
    cors = npu.to_ndim_2(cors, copy=copy)
    dim = len(vars)
    assert dim == np.shape(cors)[0] and dim == np.shape(cors)[1]
    np.fill_diagonal(cors, 1.)
    for i in range(dim):
        cors[i,:] = sds[i] * cors[i,:]
        cors[:,i] = sds[i] * cors[:,i]
    npu.lower_to_symmetric(cors, copy=False)
    return cors

def vol_to_cov(vol):
    vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=False)
    return np.dot(vol, vol.T)

def cholesky_sqrt_2d(sd1, sd2, cor):
    return np.array(((sd1, 0.), (sd2 * cor, sd2 * np.sqrt(1. - cor * cor))))

class OnlineStatsCalculator(object):
    def __init__(self, zero=0.0):
        self.reset(zero)
        
    def reset(self, zero):
        self.__n = 0
        self.__sum = zero
        self.__mean = zero
        self.__mean_sq = zero
        self.__M2 = zero
    
    @property
    def count(self):
        return self.__n
    
    @property
    def sum(self):
        return self.__sum

    @property    
    def mean(self):
        return self.__mean

    @property
    def mean_sq(self):
        return self.__mean_sq
    
    @property
    def rms(self):
        return np.sqrt(self.mean_sq)

    @property    
    def var_n(self):
        return self.__M2 / self.__n
    
    @property
    def var(self):
        return self.__M2 / (self.__n - 1)

    @property    
    def sd(self):
        return np.sqrt(self.var)

    @property    
    def sd_n(self):
        return np.sqrt(self.var_n)
    
    def add(self, x):
        self.__n += 1
        self.__sum += x
        delta = x - self.__mean
        self.__mean += delta / self.__n
        deltasq = x * x - self.__mean_sq
        self.__mean_sq += deltasq / self.__n
        if self.__n > 1:
            self.__M2 += delta * (x - self.__mean)

    def add_all(self, xs):
        for x in xs: self.add(x)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
