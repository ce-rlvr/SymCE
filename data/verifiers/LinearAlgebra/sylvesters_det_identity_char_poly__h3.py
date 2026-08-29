import sympy
from sympy import Symbol, eye, zeros, expand, simplify
from sympy.matrices import MatrixBase
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    "H_1: F is a field",
    "H_2: A is an m x n matrix over F",
    "¬Q: t^n det(tI_m - AB) != t^m det(tI_n - BA) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            A = witness[-2]
            B = witness[-1]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: F is a field
    # We verify that the elements of A belong to a commutative ring/field.
    try:
        h1 = True
        if isinstance(A, MatrixBase):
            for elem in A:
                if hasattr(elem, 'is_commutative') and not elem.is_commutative:
                    h1 = False
    except Exception:
        h1 = False

    # H2: A is an m \times n matrix over F
    try:
        h2 = isinstance(A, MatrixBase)
    except Exception:
        h2 = False

    # neg_Q: t^n \det(tI_m - AB) != t^m \det(tI_n - BA)
    try:
        m, n = A.shape
        t = Symbol('t_symb_12345', commutative=True)
        I_m = eye(m)
        I_n = eye(n)
        
        AB = A * B
        BA = B * A
        
        LHS_mat = t * I_m - AB
        RHS_mat = t * I_n - BA
        
        LHS = (t**n) * LHS_mat.det()
        RHS = (t**m) * RHS_mat.det()
        
        diff = simplify(expand(LHS - RHS))
        neg_q = bool(diff != 0)
    except Exception:
        # If matrix multiplication or determinant fails (e.g., due to shape mismatch because B is not n x m),
        # the mathematical expression is undefined, meaning the equality fails to hold.
        neg_q = True

    return [h1, h2, neg_q]