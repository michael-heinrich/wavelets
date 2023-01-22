from numpy import *
import matplotlib.pyplot as plt

# Define function to compute hydraulic heads
def fluct_head(params, x, t):
    A, omega, D = params[0], params[1], params[2]
    phi = 0
    c1 = A * exp((-x) * sqrt((omega/(2 * D))))
    c2 = sin(((-x) * sqrt(omega/(2 * D))) + (omega * t) + (phi))
    h = c1 * c2
    return h


# Fabricate observations
t = linspace(0, 31, 2**9)
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

plt.figure()
plt.plot(t, time_series)
plt.xlabel('time (days)')
plt.ylabel('head values (meters)')
plt.title('Complete signal')
plt.show()