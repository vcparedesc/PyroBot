from sympy import *

t = symbols('t')

def print_python_expr(expr, file_handler, id, X):
    F = file_handler
    rows = expr.shape[0]
    cols = expr.shape[1]
    F.write("def get_"+ id + "(x):\n\t")
    for idx in range(len(X)):
        F.write(str(X[idx]) + " = x[" + str(idx) + "]")
        F.write('\n\t')
    F.write('\n\t')
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
            F.write("\n\t")
    F.write("])")
    F.write('\n')

def print_python_dynamics(fx,gx,X,parameters, values):
    F = open("PyroDynamics.py","w")
    F.write("class PyroDynamics:\n")
    F.write('\t')
    for idx in range(len(parameters)):
        F.write(str(parameters[idx]) + " = " + str(values[idx]) + "\n\t")
    F.write("\n\t")
    print_python_expr(fx,F,"fx",X)
    F.write('\n')
    F.write('\t')
    print_python_expr(gx,F,"gx",X)
    F.close()
