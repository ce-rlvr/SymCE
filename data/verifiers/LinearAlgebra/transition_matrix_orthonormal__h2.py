import sympy
from sympy import eye, zeros, simplify, MatrixBase
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    "H_1: V is a finite-dimensional complex inner product space",
    "H_2: P is the change-of-basis matrix from B to C",
    "¬Q: P is not a unitary matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            B, C = witness
            B = sympy.Matrix(B)
            C = sympy.Matrix(C)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            B = sympy.Matrix(witness[0])
            C = sympy.Matrix(witness[1])
        else:
            B = sympy.Matrix(witness)
            C = eye(B.rows)
            
        h1 = isinstance(B, MatrixBase) and isinstance(C, MatrixBase)
    except Exception:
        h1 = False

    try:
        if h1:
            if B.shape == C.shape and B.rows == B.cols:
                detB = simplify(B.det())
                detC = simplify(C.det())
                h2 = not (detB == 0 or detB.is_zero == True) and \
                     not (detC == 0 or detC.is_zero == True)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            P = C.inv() * B
            I_mat = eye(P.rows)
            diff = P.H * P - I_mat
            is_unitary = True
            for i in range(diff.rows):
                for j in range(diff.cols):
                    val = simplify(diff[i, j])
                    if not (val == 0 or val.is_zero == True):
                        is_unitary = False
                        break
                if not is_unitary:
                    break
            neg_q = not is_unitary
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]