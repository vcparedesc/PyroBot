from sympy import *

t = symbols('t')

def print_python_expr(expr, file_handler, id, X, parameters):
    F = file_handler
    rows = expr.shape[0]
    cols = expr.shape[1]
    F.write("def get_"+ id + "(self,x):\n\t\t")
    for idx in range(len(X)):
        F.write(str(X[idx]) + " = x[" + str(idx) + "]")
        F.write('\n\t\t')
        
    for idx in range(len(parameters)):
        F.write(str(parameters[idx]) + " = self." + str(parameters[idx]))
        F.write('\n\t\t')
                
    F.write('\n\t\t')
    F.write("return np.matrix([")
    for row in range(rows):
        F.write("[")
        for col in range(cols):
            F.write(str(expr[row,col]))
            if(col <= cols - 2):
                F.write(", ")
        F.write("]")
        if(row <= rows -2):
            F.write(", ")
            F.write("\n\t\t")
    F.write("])")
    F.write('\n')

def print_python_dynamics(fx,gx,X,parameters, values):
    F = open("PyroDynamics.py","w")
    F.write("import numpy as np \n")
    F.write("from math import sin \n")
    F.write("from math import cos \n\n")
    F.write("class PyroDynamics:\n\t")
    F.write("def __init__(self):\n\t\t")
    for idx in range(len(parameters)):
        F.write("self."+str(parameters[idx]) + " = " + str(values[idx]) + "\n\t\t")
    F.write("\n\t")
    print_python_expr(fx,F,"fx",X, parameters)
    F.write('\n')
    F.write('\t')
    print_python_expr(gx,F,"gx",X, parameters)
    F.close()
