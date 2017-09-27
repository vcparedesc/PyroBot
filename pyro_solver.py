# Solving the differential equtions that represents the pendulum
# dynamics.

import numpy as np
from PyroDynamics import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt

PyroBot = PyroDynamics()
solutions = []

# Here the user defines the controller
def u_control(X,t):
    return np.matrix([[0],[0]]) # Example: state feedback

def dX(y,t):
    return np.squeeze(np.asarray(PyroBot.get_fx(y) + PyroBot.get_gx(y) * u_control(y, t)))

def simulate(X0, t):
    sol = odeint(dX, X0, t)
    solutions = sol
    for var in range(len(X0) / 2):
        plt.plot(t, sol[:,var], label = 'x' + str(var + 1))
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()
    for var in range(len(X0) / 2):
        plt.plot(t, sol[:,var + len(X0) / 2], label = 'xd' + str(var + 1))
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()

    return sol

