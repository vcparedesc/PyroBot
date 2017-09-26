# License to be added
# Extending sympy definitions to allow to work with robot dynamics

from sympy import *

t = symbols('t')

# This operation takes an scalar and returns a vector(Matrix) of the size of Q
def diff_wrt_vector(expr, Q):
    l = len(Q)
    M = zeros(l,1)
    for row in range(l):
        M[row] = diff(expr, Q[row])
    return M

def diff_vector_wrt_vector(vector, Q):
    l = len(Q)
    M = zeros(vector.shape[0], l)
    for row in range(vector.shape[0]):
        for col in range(l):
            M[row, col] = diff(vector[row], Q[col])
    return M

    
