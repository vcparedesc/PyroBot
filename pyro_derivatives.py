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

# lie_derivative_Lf: Computes the lie derivative of vector along fx. Lf(vector)
# @vector: is the vector taken to compute the lie derivative
# @stateX: The state vector from which partial derivative will be calculated
# @fx: The dynamic vector fx
def lie_derivative_Lf(vector, stateX, fx):
    return diff_vector_wrt_vector(vector, stateX) * fx

# lie_derivative_Lg: Computes the lie derivative of vector along gx. Lg(vector)
# @vector: is the vector taken to compute the lie derivative
# @stateX: The state vector from which partial derivative will be calculated
# @gx: The dynamic vector gx
def lie_derivative_Lg(vector, stateX, gx):
    return diff_vector_wrt_vector(vector, stateX) * gx

# lie_derivative_Lfn: Computes the n-lie derivative of vector along fx. Lf^n(vector)
# @vector: is the vector taken to compute the lie derivative
# @stateX: The state vector from which partial derivative will be calculated
# @fx: The dynamic vector fx
# @n: The number of times lie derivative is taken
def lie_derivative_Lfn(vector, stateX, fx, n):
    result = vector
    for k in range(n):
        result = lie_derivative_Lf(result, stateX, fx)
    return result

# lie_derivative_LgLfn: Computes the (n-1)-lie derivative of vector along fx and one lie derivative wrt gx. LgLf^(n-1)(vector)
# @vector: is the vector taken to compute the lie derivative
# @stateX: The state vector from which partial derivative will be calculated
# @fx: The dynamic vector fx
# @gx: The dynamic vector gx
# @n: The number of times lie derivative is taken
def lie_derivative_LgLfn(vector, stateX, fx, gx, n):
    result = lie_derivative_Lfn(vector, stateX, fx, n - 1)
    return lie_derivative_Lg(result, stateX, gx)
    
