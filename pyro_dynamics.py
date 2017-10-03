from pyro_derivatives import *
t = symbols('t')

def lagrange_method(L,Q):
    Qd = diff(Q,t,1)
    EoM = simplify(diff((diff_wrt_vector(L,Qd)),t)-diff_wrt_vector(L,Q))
    return EoM

def get_matrix_M(EoM, Q):
    Qd = diff(Q,t,1)
    Qdd = diff(Q,t,2)
    Mat_M = simplify(diff_vector_wrt_vector(EoM, Qdd))
    return Mat_M

def get_fx_gx(EoM, Q):
    Qd = diff(Q,t,1)
    Qdd = diff(Q,t,2)
    l = len(Q)
    fx = zeros(2*l,1)
    gx = zeros(2*l,l)
    Mat_M = get_matrix_M(EoM, Q)
    fx[0,0] = Qd
    fx[l,0] = simplify(Mat_M.inv() * simplify(Mat_M * Qdd - EoM))
    gx[0,0] = zeros(l,l)
    gx[l,0] = Mat_M.inv();
    return (fx,gx)

def change_vars(expr, oldVar, newVar):
    l = len(oldVar)
    nexpr = expr
    for idx in range(l):
        nexpr = nexpr.subs(oldVar[l - idx - 1], newVar[l - idx - 1])
    return nexpr
