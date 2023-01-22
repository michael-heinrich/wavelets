
import unittest

import sys

from numpy import *
import matplotlib.pyplot as plt
from dwt.modwt.modwt import *


for p in sys.path:
    ind = p.find("/dwt/")
    if ind >= 0:
        sys.path.append(p[0:ind])
        break


# Define function to compute hydraulic heads
def fluct_head(params, x, t):
    A, omega, D = params[0], params[1], params[2]
    phi = 0
    c1 = A * exp((-x) * sqrt((omega/(2 * D))))
    c2 = sin(((-x) * sqrt(omega/(2 * D))) + (omega * t) + (phi))
    h = c1 * c2
    return h

# Fabricate observations
# Return tuple with attributes:
#   time_series
#   levels


def get_fabricated_observations_long():
    levels = 9
    t = linspace(0, 31, 2**levels)
    b = 10                                 # saturated aquifer thickness [m]
    Sy = 0.1                               # specific yield [-]
    K = 10
    D = (K * b) / Sy

    x = 10

    # Wave 1
    A1 = 1
    omega1 = 2 * pi / 7
    params1 = [A1, omega1, D]

    # Wave 2
    A2 = 0.3
    omega2 = pi
    params2 = [A2, omega2, D]

    time_series = fluct_head(params1, x, t) + fluct_head(params2, x, t)

    return (time_series, levels)


def get_fabricated_observations_short():
    levels = 3
    time_series = np.arange(10)

    return (time_series, levels)


def reconstruct_signal(mra_series):
    return sum(mra_series, axis=0)


class TestDwt(unittest.TestCase):

    # make sure that the test framework is working
    def test_framework(self):
        print("test_framework")

    def test_circular_convolve_no_pad(self):
        x = np.array([1, 2, 3])
        y = np.array([0, 1, 0.5])
        expected_output = [4., 2.5, 2.5]
        res = circular_convolve_no_pad(x, y)
        print("expected_output: ", expected_output)
        print("res: ", res)
        self.assertEqual(res, expected_output)

    def test_circular_convolve_no_pad_int(self):
        x = np.array([1, 2, 3])
        y = np.array([0, 1, 0.5])
        expected_output = [4, 2, 2]
        res = circular_convolve_no_pad_int(x, y)
        print("expected_output: ", expected_output)
        print("res: ", res)
        self.assertEqual(res, expected_output)

    def test_circular_convolve_mra(self):
        x = np.array([1, 2, 3])
        y = np.array([0, 1, 0.5])
        expected_output = circular_convolve_no_pad_int(x, y)
        res = circular_convolve_mra(x, y)
        print("expected_output: ", expected_output)
        print("res: ", res)
        self.assertEqual(res, expected_output)



    def test_dwt_short(self):
        print("test_dwt_short")
        time_series, levels = get_fabricated_observations_short()
        print("time_series: ", time_series)
        dwt_series = modwt(time_series, 'db2', levels)
        mra_series = modwtmra(dwt_series, 'db2')
        print("mra_series: ", mra_series)
        print(sum(mra_series, axis=0))

    def test_dwt_short_nonzero(self):
        print("test_dwt_short_nonzero")
        time_series, levels = get_fabricated_observations_short()
        print("time_series: ", time_series)
        dwt_series = modwt(time_series, 'db2', levels)
        mra_series = modwtmra(dwt_series, 'db2')
        print("mra_series: ", mra_series)

        reconstructed = reconstruct_signal(mra_series)

        # make sure at least one element of mra_series is nonzero
        print(reconstructed)
        self.assertTrue(reconstructed.any())

    def test_dwt_long_nonzero(self):
        print("test_dwt_short_nonzero")
        time_series, levels = get_fabricated_observations_long()
        print("time_series: ", time_series)
        dwt_series = modwt(time_series, 'haar', levels)
        mra_series = modwtmra(dwt_series, 'haar')
        print("mra_series: ", mra_series)

        reconstructed = reconstruct_signal(mra_series)

        # make sure at least one element of mra_series is nonzero
        print(reconstructed)
        self.assertTrue(reconstructed.any())

    # check if the reconstructed time series is the same as the original

    def test_reconstruct_short(self):
        print("test_reconstruct_short")
        time_series, levels = get_fabricated_observations_short()
        print("time_series: ", time_series)
        dwt_series = modwt(time_series, 'db2', levels)
        mra_series = modwtmra(dwt_series, 'db2')
        print("mra_series: ", mra_series)

        reconstructed = reconstruct_signal(mra_series)

        # make sure at least one element of mra_series is nonzero
        print(reconstructed)
        self.assertTrue(reconstructed.any())

        # make sure the reconstructed series is the same as the original
        self.assertTrue(np.array_equal(time_series, reconstructed))

    # check if the reconstructed time series is the same as the original

    def test_reconstruct_long(self):
        print("test_reconstruct_long")
        time_series, levels = get_fabricated_observations_long()
        print("time_series: ", time_series)
        dwt_series = modwt(time_series, 'haar', levels)
        mra_series = modwtmra(dwt_series, 'haar')
        print("mra_series: ", mra_series)

        reconstructed = reconstruct_signal(mra_series)

        # make sure at least one element of mra_series is nonzero
        print(reconstructed)
        self.assertTrue(reconstructed.any())

        # make sure the reconstructed series is the same as the original
        self.assertTrue(np.array_equal(time_series, reconstructed))
