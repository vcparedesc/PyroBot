from pyro_derivatives import *
from pyro_kinematics import *
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

def robot_Dmat(DH, Masses, Inertias, CoMs):
    sz = DH.shape[0]
    Dmat = zeros(sz, sz)
    for link_i in range(sz):
        Jacob = JacobianDH_CoM(DH, link_i + 1, CoMs) # Joint i + 1
        mass = Masses[link_i]
        InertiaCoM = Inertias[3 * link_i: 3 * (link_i + 1), 0:3]
        R = TransformationDH(DH, link_i)[0:3,0:3] # Link i
        Dmat = Dmat + mass * Jacob[0:3, 0:sz].T * Jacob[0:3, 0:sz]  + Jacob[3:6, 0:sz].T * R * InertiaCoM * R.T * Jacob[3:6, 0:sz]
    return simplify(Dmat)

def christoffel1(Dmat, DH, i, j, k):
    chris = 0.5 * (diff(Dmat[k,j], DH[i,3]) + diff(Dmat[k,i], DH[j, 3]) - diff(Dmat[i,j], DH[k ,3]))
    return chris

def robot_Cmat(Dmat, DH):
    sz = Dmat.shape[0]
    Cmat = zeros(sz,sz)
    for k in range(sz):
        for j in range(sz):
            for i in range(sz):
                Cmat[k,j] = Cmat[k,j] + christoffel1(Dmat, DH, i, j, k) * diff(DH[i,3],t)
    return simplify(Cmat)

# robot_Gmat: Computes the gravity vector in the equation of motion (Dqdd + Cqd + G = Tau)
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @g: Represents the gravity vector in three dimensions, for instance: g = Matrix([ [0], [0], [-9.81] })
def robot_Gmat(DH, g, Masses, CoMs):
    sz = DH.shape[0]
    PotEnergy = Matrix([[0]])
    Gmat = zeros(sz, 1)
    for dof in range(sz):
        mass = Masses[dof]
        PotEnergy = PotEnergy + mass * g.T * Vector_PosFrameDH(DH, dof + 1,CoMs[dof,:].T)

    for dof in range(sz):
        Gmat[dof] = diff(PotEnergy, DH[dof, 3])
    return simplify(Gmat)

def robot_dynamics(DH,g, Masses, Inertias, CoMs):
    Dmat = robot_Dmat(DH, Masses, Inertias, CoMs)
    Cmat = robot_Cmat(Dmat, DH)
    Gmat = robot_Gmat(DH, g, Masses, CoMs)
    return (Dmat, Cmat, Gmat)
