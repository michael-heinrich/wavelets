from numpy import *
import matplotlib.pyplot as plt
from modwt import *
import pywt

# Define function to compute hydraulic heads
def fluct_head(params, x, t):
    A, omega, D = params[0], params[1], params[2]
    phi = 0
    c1 = A * exp((-x) * sqrt((omega/(2 * D))))
    c2 = sin(((-x) * sqrt(omega/(2 * D))) + (omega * t) + (phi))
    h = c1 * c2
    return h


# Fabricate observations
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

trafo = pywt.swt(time_series, 'haar', level=9, norm=True)
print(len(trafo))
plt.plot(trafo[0][0])
plt.plot(trafo[0][1])
plt.plot(trafo[1][0])
plt.plot(trafo[1][1])
plt.plot(trafo[2][0])
plt.plot(trafo[2][1])
plt.plot(trafo[3][0])
plt.plot(trafo[3][1])





plt.figure()
plt.plot(t, time_series)
plt.xlabel('time (days)')
plt.ylabel('head values (meters)')
plt.title('Complete signal')



dwt_series = modwt(time_series, 'haar', levels)
dwt_series = modwtmra(dwt_series, 'haar')
plt.figure()
for level in range(levels):
    plt.plot(dwt_series[level], label='level' + str(level))
plt.xlabel('time (days)')
plt.ylabel('head values (meters)')
plt.title('DWT of signals')
plt.legend()



s1 = np.arange(10)
print(s1)
ws = modwt(s1, 'db2', 3)
mra = modwtmra(ws, 'db2')
print(mra)
print(sum(mra, axis=0))
plt.figure()
for level in range(3):
    plt.plot(mra[level], label='level' + str(level))
plt.xlabel('index')
plt.ylabel('values')
plt.title('DWT of short signal')
plt.legend()
plt.show()