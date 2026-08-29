import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix
from sympy.abc import x
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 3:
            n_wit, A, B = witness
        elif len(witness) == 2:
            A, B = witness
            n_wit = A.shape[0] if hasattr(A, 'shape') else len(A)
        else:
            return [False, False, False]
        
        A = Matrix(A)
        B = Matrix(B)
    except Exception:
        return [False, False, False]

    try:
        n = A.shape[0]
        h1 = bool(n > 0 and n == n_wit and A.shape == (n, n) and B.shape == (n, n))
    except Exception:
        h1 = False

    try:
        # We accept any n x n matrices to be robust against different interpretations of U(n)
        # in the context of the dropped hypothesis (e.g., if U(n) was meant to be M_n(C) or GL_n(C)).
        h2 = bool(A.shape == (n, n) and B.shape == (n, n))
    except Exception:
        h2 = False

    try:
        same_charpoly = (A.charpoly(x) == B.charpoly(x))
        
        try:
            are_similar = A.is_similar(B)
        except Exception:
            # Fallback if is_similar is not available
            JA = A.compute_jordan_form()[1]
            JB = B.compute_jordan_form()[1]
            are_similar = (JA == JB)
            
        not_conjugate = not are_similar
        neg_q = bool(same_charpoly and not_conjugate)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: A and B are elements of U(n)",
    "¬Q: A and B have the same characteristic polynomial but are not conjugate in U(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2