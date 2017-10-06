import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import *
import numpy as np

Animatrix = []
COMindex = []
PoseX = []
PoseY = []
PoseZ = []

fig_anim = []
line = []
time_text = []
time_template = []
ax = []

def fireAnimation(animationMatrix, idCOM, q_var, q_value, parameters, values):
    global Animatrix, Idcom, line, time_template, time_text, fig_anim, ax

    Animatrix = animationMatrix
    COMindex = idCOM
    
    evaluatePose(q_var, q_value, parameters, values)

    fig_anim = plt.figure()
    ax = fig_anim.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax.grid()

    line, = ax.plot([], [], lw=2)
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    ani = animation.FuncAnimation(fig_anim, animator, np.arange(1, PoseX.shape[1]),
                                  interval = 25, blit = True, init_func = init)
    plt.show()

    return ani



def evalVars(matrix, q_var, q_value_x, parameters, values):
    vMat = matrix
    for i in range(len(q_var)):
        vMat = vMat.subs(q_var[i], q_value_x[i])
    for i in range(len(parameters)):
        vMat = vMat.subs(parameters[i], values[i])
    return vMat

def evaluatePose(q_var, q_value, parameters, values):
    global PoseX, PoseY, PoseZ

    PoseX = zeros(Animatrix.shape[0],q_value.shape[0])
    PoseY = zeros(Animatrix.shape[0],q_value.shape[0])
    PoseZ = zeros(Animatrix.shape[0],q_value.shape[0])

    for i in range(q_value.shape[0]):
        PoseX[0,i] = evalVars(Animatrix[:,0], q_var, q_value[i,:], parameters, values)
        PoseY[0,i] = evalVars(Animatrix[:,1], q_var, q_value[i,:], parameters, values)
        PoseZ[0,i] = evalVars(Animatrix[:,2], q_var, q_value[i,:], parameters, values)

def init():
    global line, time_text
    print "Init"
    line.set_data([],[])
    time_text.set_text('')
    return line, time_text

def animator(i):
    global line, time_text, time_template

    print "PoseX:"

    thisx =  flatten(PoseX[:,i].T)
    thisy =  flatten(PoseY[:,i].T)

    print PoseX

    line.set_data(thix, thisy)
    # time_text.set_text(time_template % (i * ))
    return line, time_text


