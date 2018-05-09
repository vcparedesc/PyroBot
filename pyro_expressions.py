from sympy import *

t = symbols('t')

# change_vars: changes the variables of a mathematical expression
# @expr: Original expression with variables described in list oldVar
# @oldVar: Specifies the list of variables that the expression expr have
# @newVar: Specifies the new list of variables taht the epxression expr will have
def change_vars(expr, oldVar, newVar):
    l = len(oldVar)
    nexpr = expr
    for idx in range(l):
        nexpr = nexpr.subs(oldVar[l - idx - 1], newVar[l - idx - 1])
    return nexpr

# print_python_expr: Prints the symbolic operation of a single matrix expression in python
# @expr: Expression that will be write into a numpy matrix
# @file_handler: Receives the file handler to perform a writing operation on the file
# @id: Expression name, it is a string
# @X: variables that will be used to construct the file
# @parameters: List of parameters that will be read from the global ones
def print_python_expr(expr, file_handler, id, X, parameters):
    F = file_handler
    rows = expr.shape[0]
    cols = expr.shape[1]
    F.write("def get_"+ id + "(self,x,t):\n\t\t")
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

# print_python_dynamics: Writes the dynamic matrices fx and gx for fast python computation
# @fx: dynamic matrix
# @gx: dynamic matrix
# @TQ: Tangent bundle with current variables used
# @X: State vector with new desired variables
# @parameters: List of parameters that will be read from the global ones
# @values: List of parameters' values in same order that list "parameters"
def print_python_dynamics(fx,gx,TQ,X,parameters, values):
    print_python_matrices([fx,gx], ["fx","gx"], TQ, X, parameters, values, "PyroBot")

# print_python_matrices: Writes a list of mathematical expressions for fast python computation
# @ExprList: List of the expressions to be written. E.g: [fx, gx]
# @ExprNames: List of the expression names to be written as class members. E.g ["name1", "name2"]
# @BundleTQ: List of current variables describing the tangent bundle. [q1,q2,derivative(q1), derivative(q2)]
# @StateX: List of new states that will be used to write the matrix expressions
# @parameters: List of parameters that will be read from the global ones
# @parameters_values: List of parameters' values in same order that list "parameters"
# @filename: The name of python file and the created classn
def print_python_matrices(ExprList, ExprNames, BundleTQ, StateX, parameters, parameters_values, filename):    
    F = open(filename + ".py", "w")
    F.write("import numpy as np \n")
    F.write("from math import sin \n")
    F.write("from math import cos \n\n")
    F.write("class " +  filename + ":\n\t")
    F.write("def __init__(self):\n\t\t")
    for idx in range(len(parameters)):
        F.write("self."+str(parameters[idx]) + " = " + str(parameters_values[idx]) + "\n\t\t")
    F.write("\n\t")
    for idx in range(len(ExprList)):       
        print_python_expr(change_vars(ExprList[idx], BundleTQ, StateX),F,ExprNames[idx],StateX, parameters)
        F.write('\n')
        F.write('\t')
    F.close()

