import matplotlib.pyplot as plt
from matplotlib import animation, rc
from sympy import *
import numpy as np
from IPython.display import HTML

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
ani = []
delta_time = []

def init():
    global line, time_text
    line.set_data([],[])
    time_text.set_text('')
    return line, time_text

def animator(i):
    global line, time_text, time_template
    thisx =  flatten(PoseX[:,i].T)
    thisy =  flatten(PoseY[:,i].T)
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i * delta_time))
    return line, time_text

def fireAnimation(animationMatrix, idCOM, q_var, q_value, parameters, values, dt):
    global Animatrix, Idcom, line, time_template, time_text, fig_anim, ax, ani, delta_time
    delta_time = dt
    
    Animatrix = animationMatrix
    COMindex = idCOM
    evaluatePose(Animatrix, q_var, q_value, parameters, values)
    fig_anim = plt.figure()
    ax = fig_anim.add_subplot(111, autoscale_on=False, xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
    ax.grid()
    line, = ax.plot([], [],'o-',lw=2)
    ax.set_aspect('equal')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    rc('animation', html='html5')
    ani = animation.FuncAnimation(fig_anim, animator, np.arange(1, PoseX.shape[1]), interval = delta_time * 1000, blit = True, init_func = init)
    #ani.save("animationVid.mp4", fps = 30, extra_args=['-vcodec', 'libx264'])
    #plt.show()

    return ani

def evalVars(matrix, q_var, q_value_x, parameters, values):
    vMat = matrix
    for i in range(len(q_var)):
        vMat = vMat.subs(q_var[i], q_value_x[i])
    for i in range(len(parameters)):
        vMat = vMat.subs(parameters[i], values[i])
    return vMat

def evaluatePose(matrix,q_var, q_value, parameters, values):
    global PoseX, PoseY, PoseZ
    PoseX = zeros(matrix.shape[0],q_value.shape[0])
    PoseY = zeros(matrix.shape[0],q_value.shape[0])
    PoseZ = zeros(matrix.shape[0],q_value.shape[0])
    for i in range(q_value.shape[0]):
        PoseX[0,i] = evalVars(matrix[:,0], q_var, q_value[i,:], parameters, values)
        PoseY[0,i] = evalVars(matrix[:,1], q_var, q_value[i,:], parameters, values)
        PoseZ[0,i] = evalVars(matrix[:,2], q_var, q_value[i,:], parameters, values)
    return PoseX, PoseY, PoseZ

