import sympy
from sympy import eye, zeros, simplify, Matrix
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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
    "H_1: lambda is an eigenvalue of A with algebraic multiplicity a and geometric multiplicity g",
    "¬Q: The sum of (s_i - 1) over all Jordan blocks of size s_i corresponding to lambda is NOT exactly equal to the defect a - g"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            A, lambda_val = witness
            check_all = False
        else:
            A = witness
            check_all = True
    except Exception:
        return [False, False]

    try:
        evs = A.eigenvects()
        if check_all:
            h1 = len(evs) > 0
        else:
            h1 = False
            for ev, alg_mult, evecs in evs:
                if ev == lambda_val or simplify(ev - lambda_val) == 0:
                    h1 = True
                    a = alg_mult
                    g = len(evecs)
                    break
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            P, J = A.jordan_form()
            if check_all:
                neg_q = False
                for ev, alg_mult, evecs in evs:
                    l_val = ev
                    a_val = alg_mult
                    g_val = len(evecs)
                    sum_s = 0
                    for i in range(J.shape[0] - 1):
                        if (J[i, i] == l_val or simplify(J[i, i] - l_val) == 0) and \
                           (J[i+1, i+1] == l_val or simplify(J[i+1, i+1] - l_val) == 0) and \
                           (J[i, i+1] == 1 or simplify(J[i, i+1] - 1) == 0):
                            sum_s += 1
                    if sum_s != a_val - g_val:
                        neg_q = True
                        break
            else:
                sum_s = 0
                for i in range(J.shape[0] - 1):
                    if (J[i, i] == lambda_val or simplify(J[i, i] - lambda_val) == 0) and \
                       (J[i+1, i+1] == lambda_val or simplify(J[i+1, i+1] - lambda_val) == 0) and \
                       (J[i, i+1] == 1 or simplify(J[i, i+1] - 1) == 0):
                        sum_s += 1
                neg_q = (sum_s != a - g)
    except Exception:
        neg_q = False

    return [h1, neg_q]