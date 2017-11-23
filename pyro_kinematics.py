from sympy import *
t = symbols('t')
revolute = Matrix([['r']])[0]
prismatic = Matrix([['p']])[0]

# Rot: Compute the rotation matrix given an axis and an angle.
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @angle: Expressed in radians it specifies the rotation angle.
def Rot(axis, angle):
    if axis == 'x':
        return Matrix([ [1,0,0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)] ])
    elif axis == 'y':
        return Matrix([ [cos(angle), 0, sin(angle)], [0,1,0], [-sin(angle), 0, cos(angle)] ])
    elif axis == 'z':
        return Matrix([ [cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0,0,1]])
    else:
        cs = cos(angle)
        sn = sin(angle)
        v = 1 - cos(angle)
        kx = axis[0]
        ky = axis[1]
        kz = axis[2]
        return Matrix([ [kx**2 * v + cs, kx*ky*v-kz*sn, kx*kz*v+ky*sn],
                        [kx*ky*v+kz*sn, ky**2*v+cs, ky*kz*v-kx*sn],
                        [kx*kz*v-ky*sn, ky*kz*v+kx*sn, kz**2*v+cs]])

# Pos: Compute the position vector (matrix) given an axis and a distance vector.
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @distance: An scalar that specifies the distance of movement along the axis.
def Pos(axis, distance):
    DV = zeros(3,1)
    if axis == 'x':
        DV = Matrix([ [distance], [0], [0] ])
    elif axis == 'y':
        DV = Matrix([ [0], [distance], [0] ])
    elif axis == 'z':
        DV = Matrix([ [0], [0], [distance] ])
    elif len(distance) == 3:
        DV = distance
    elif len(distance) == 4:
        DV = distance[0:3,0]
    else:
        DV = distance * axis
    return DV

# PosH: Compute the homogeneous position vector (matrix) given an axis and a distance vector.
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @distance: An scalar that specifies the distance of movement along the axis.
def PosH(axis, distance):
    PosH = ones(4,1)
    PosH[0,0] = Pos(axis, distance)
    return PosH

# Hom: Compute the homogeneous matrix given an axis, a distance vector and an angle.
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @angle: Expressed in radians it specifies the rotation angle.
# @distance: An scalar that specifies the distance of movement along the axis.
def Hom(axis, angle, distance):
    HM = eye(4)
    HM[0,0] = Rot(axis,angle)
    HM[0,3] = Pos(axis, distance)
    return HM

# Hom: Compute the homogeneous matrix given an axis and an angle. Assumming
# there is no displacement
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @angle: Expressed in radians it specifies the rotation angle.
def HomR(axis,angle):
    HM = Hom(axis,angle,0)
    return HM

# Hom: Compute the homogeneous matrix given an axis and a distance vector. Assumming
# there is no rotation
# @axis: It can be specified as a vector or specified as 'x', 'y' or 'z'.
# @distance: An scalar that specifies the distance of movement along the axis.
def HomT(axis,distance):
    HM = Hom(axis, 0, distance)
    return HM

# Skew: Computes an skew matrix from a vector,
# @vector: A 3-dim vector (3,1) or the euclidean common axis 'x', 'y' or 'z'.
def Skew(vector):
    if(vector == 'x'):
        return Matrix([ [0,0,0], [0,0,-1], [0,1,0] ])
    elif(vector == 'y'):
        return Matrix([ [0,0,1], [0,0,0], [-1,0,0] ])
    elif(vector == 'z'):
        return Matrix([ [0,-1,0], [1,0,0], [0,0,0] ])
    else:
        ax = vector[0]
        ay = vector[1]
        az = vector[2]
        return Matrix([ [0, -az, ay], [az, 0, ax], [-ay, ax, 0] ])

# AxisZ: Computes the vector that describes the rotation axis (z) from the DH table.
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @i: Represents the joint number which is required to obtain the Z-axis. (Joints start at 0)
def AxisZ(DH, i):
    sz = DH.shape[0]
    if (i > sz):
        print("Joint number is out of bounds - AxisZ")
        return 0
    elif i == 0:
        R = eye(3)
        return R[:,2]
    else:
        R = eye(3)
        for link in range(i):
            R = simplify(R * Rot('z', DH[link, 3]))
        return R[:,2]
 
# PosFrameDH: Computes the vector that describes the position of a Joint given the DH table.
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @i: Represents the joint number which is required to obtain the position. (Joints start at 0)   
def PosFrameDH(DH, i):
    sz = DH.shape[0]
    if (i > sz):
        print("Joint number is out of bounds - PosFrameDH")
        return 0
    elif i == 0:
        return zeros(3,1)
    else:
        Pos = zeros(3,1)
        T = eye(4)
        for link in range(i):
            T = simplify(T * TransformationDH(DH,link))
        return T[0:3,3]
     
# TransformationDH: Computes the transformation matrix of link: i wrt link: i + 1 (i + 1 wrt i?)
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @i: Represents the link number where the transformation is required
def TransformationDH(DH, i):
    sz = DH.shape[0]
    if (i >= sz):
        print("Link number is out of bounds - TransformationDH")
        return 0
    else:
        return simplify(HomR('z', DH[i, 3]) * HomT('z', DH[i, 2]) * HomT('x', DH[i, 0]) * HomR('x', DH[i, 1]))

# JacobianDH: Computes the jacobian matrix of joint: i
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @i: Represents the joint number where the jacobian is required
def JacobianDH(DH, i):
    sz = DH.shape[0]
    Jw = zeros(3, sz)
    Jv = zeros(3, sz)
    if i > sz:
        print("Joint number is out of bounds - JacobianDH")
        return 0
    else:
        for link in range(i):
            if (DH[link, 4] == revolute):
                Jw[0, link] = AxisZ(DH,link)
                Jv[0, link] = Skew(AxisZ(DH,link)) * (PosFrameDH(DH, sz) - PosFrameDH(DH, link))
            elif (DH[link, 4] == prismatic):
                Jw[0, link] = Matrix([[0], [0], [0]])
                Jv[0, link] = AxisZ(DH,link)
        return Matrix([Jv,Jw])

def JacobianvDH(DH, i):
    sz = DH.shape[0]
    return JacobianDH(DH,i)[0:3, 0:sz]

def JacobianwDH(DH, i):
    sz = DH.shape[0]
    return JacobianDH(DH, i)[3:6, 0:sz]

# JointKin: Computes the transformation matrix related to Joint i
# @DH: Denavit hartenberg table: Matrix([ [a1, alfa1, d1, theta1, 'r'], [a2, alfa2, d2, theta2, 'p'], ... ])
# where: a, alfa, d, theta are the DH parameters, 'r' means a rotational joint and 'p' a prismatic one
# @i: Represents the joint number where the transformation matrix is required    
def JointKin(DH, i):
    sz = DH.shape[0]
    if i > sz:
        print("Joint number is out of bounds - JointKin")
        return 0
    T = eye(4)
    for i in range(i):
        T = T * TransformationDH(DH, i)
    return T       
