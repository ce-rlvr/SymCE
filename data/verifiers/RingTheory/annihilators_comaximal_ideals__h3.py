import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: I and J are ideals of R",
    "¬Q: Ann_M(I \\cap J) != Ann_M(I) + Ann_M(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_ring(size, add, mul):
    if size <= 0: return False
    for i in range(size):
        for j in range(size):
            if not (0 <= add[i][j] < size): return False
            if not (0 <= mul[i][j] < size): return False
    for i in range(size):
        for j in range(size):
            if add[i][j] != add[j][i]: return False
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
    zero = -1
    for i in range(size):
        if all(add[i][j] == j for j in range(size)):
            zero = i
            break
    if zero == -1: return False
    for i in range(size):
        if not any(add[i][j] == zero for j in range(size)): return False
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
    for i in range(size):
        for j in range(size):
            if mul[i][j] != mul[j][i]: return False
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
    identity = -1
    for i in range(size):
        if all(mul[i][j] == j for j in range(size)):
            identity = i
            break
    if identity == -1: return False
    return True

def check_module(R_size, R_add, R_mul, M_size, M_add, M_rmul):
    if M_size <= 0: return False
    for i in range(M_size):
        for j in range(M_size):
            if not (0 <= M_add[i][j] < M_size): return False
    for i in range(R_size):
        for j in range(M_size):
            if not (0 <= M_rmul[i][j] < M_size): return False
    for i in range(M_size):
        for j in range(M_size):
            if M_add[i][j] != M_add[j][i]: return False
    for i in range(M_size):
        for j in range(M_size):
            for k in range(M_size):
                if M_add[M_add[i][j]][k] != M_add[i][M_add[j][k]]: return False
    zero = -1
    for i in range(M_size):
        if all(M_add[i][j] == j for j in range(M_size)):
            zero = i
            break
    if zero == -1: return False
    for i in range(M_size):
        if not any(M_add[i][j] == zero for j in range(M_size)): return False
    
    R_id = -1
    for i in range(R_size):
        if all(R_mul[i][j] == j for j in range(R_size)):
            R_id = i
            break
    if R_id == -1: return False
    
    for r in range(R_size):
        for m1 in range(M_size):
            for m2 in range(M_size):
                if M_rmul[r][M_add[m1][m2]] != M_add[M_rmul[r][m1]][M_rmul[r][m2]]: return False
    for r1 in range(R_size):
        for r2 in range(R_size):
            for m in range(M_size):
                if M_rmul[R_add[r1][r2]][m] != M_add[M_rmul[r1][m]][M_rmul[r2][m]]: return False
    for r1 in range(R_size):
        for r2 in range(R_size):
            for m in range(M_size):
                if M_rmul[R_mul[r1][r2]][m] != M_rmul[r1][M_rmul[r2][m]]: return False
    for m in range(M_size):
        if M_rmul[R_id][m] != m: return False
    return True

def check_ideal(R_size, R_add, R_mul, I):
    if not I: return False
    I_set = set(I)
    for i in I:
        for j in I:
            if R_add[i][j] not in I_set: return False
    zero = -1
    for i in range(R_size):
        if all(R_add[i][j] == j for j in range(R_size)):
            zero = i
            break
    if zero == -1: return False
    for i in I:
        has_inv = False
        for j in I:
            if R_add[i][j] == zero:
                has_inv = True
                break
        if not has_inv: return False
    for i in I:
        for r in range(R_size):
            if R_mul[r][i] not in I_set: return False
    return True

def get_annihilator(M_size, M_rmul, ideal, M_zero):
    ann = []
    for m in range(M_size):
        is_ann = True
        for i in ideal:
            if M_rmul[i][m] != M_zero:
                is_ann = False
                break
        if is_ann:
            ann.append(m)
    return set(ann)

def check_conclusion(R_size, R_add, R_mul, M_size, M_add, M_rmul, I, J):
    I_set = set(I)
    J_set = set(J)
    intersect = I_set.intersection(J_set)
    
    M_zero = -1
    for i in range(M_size):
        if all(M_add[i][j] == j for j in range(M_size)):
            M_zero = i
            break
    if M_zero == -1: return False
            
    ann_I = get_annihilator(M_size, M_rmul, I_set, M_zero)
    ann_J = get_annihilator(M_size, M_rmul, J_set, M_zero)
    ann_intersect = get_annihilator(M_size, M_rmul, intersect, M_zero)
    
    sum_ann = set()
    for m1 in ann_I:
        for m2 in ann_J:
            sum_ann.add(M_add[m1][m2])
            
    return ann_intersect == sum_ann

def conditions(witness):
    """
    witness should be a dictionary with the following keys:
    - R_size: int
    - R_add: 2D list of ints (size R_size x R_size)
    - R_mul: 2D list of ints (size R_size x R_size)
    - M_size: int
    - M_add: 2D list of ints (size M_size x M_size)
    - M_rmul: 2D list of ints (size R_size x M_size)
    - I: list of ints (elements of ideal I)
    - J: list of ints (elements of ideal J)
    """
    try:
        if isinstance(witness, dict):
            R_size = witness['R_size']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            M_size = witness['M_size']
            M_add = witness['M_add']
            M_rmul = witness['M_rmul']
            I = witness['I']
            J = witness['J']
        else:
            R_size = witness.R_size
            R_add = witness.R_add
            R_mul = witness.R_mul
            M_size = witness.M_size
            M_add = witness.M_add
            M_rmul = witness.M_rmul
            I = witness.I
            J = witness.J
            
        if R_size > 100 or M_size > 100:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = check_ring(R_size, R_add, R_mul)
    except Exception:
        h1 = False

    try:
        h2 = check_module(R_size, R_add, R_mul, M_size, M_add, M_rmul)
    except Exception:
        h2 = False

    try:
        h3 = check_ideal(R_size, R_add, R_mul, I) and check_ideal(R_size, R_add, R_mul, J)
    except Exception:
        h3 = False

    try:
        neg_q = not check_conclusion(R_size, R_add, R_mul, M_size, M_add, M_rmul, I, J)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]