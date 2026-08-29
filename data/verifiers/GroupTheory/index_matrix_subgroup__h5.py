import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    A = None
    H = None
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, H = witness
        else:
            A = witness
    except Exception:
        pass

    # H_1: Let n be a positive integer.
    try:
        n = A.rows
        h1 = (n > 0)
    except Exception:
        h1 = False

    # H_2: Let G be the free abelian group Z^n.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: Let A be an n x n matrix with integer entries.
    try:
        h3 = (A.cols == n) and all(
            isinstance(v, (int, sympy.Integer)) or (hasattr(v, 'is_integer') and v.is_integer) 
            for v in A
        )
    except Exception:
        h3 = False

    # H_4: Let the determinant of A be non-zero.
    try:
        h4 = (A.det() != 0)
    except Exception:
        h4 = False

    # ¬Q: The index of H in G is NOT finite or NOT equal to the absolute value of the determinant of A.
    try:
        if H is None:
            neg_q = False
        else:
            if not isinstance(H, sympy.Matrix):
                H = sympy.Matrix(H)
            
            if H.rows != n and H.cols == n:
                H = H.T
            
            if H.rows != n:
                idx = float('inf')
            elif H.cols < n:
                idx = float('inf')
            elif H.cols == n:
                d = H.det()
                idx = abs(d) if d != 0 else float('inf')
            else:
                try:
                    from sympy.matrices.normalforms import smith_normal_form
                    S = smith_normal_form(H)
                    idx = 1
                    for i in range(n):
                        if S[i, i] == 0:
                            idx = float('inf')
                            break
                        idx *= abs(S[i, i])
                except Exception:
                    idx = float('inf')
            
            det_A = abs(A.det())
            q = (idx != float('inf')) and (idx == det_A)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the free abelian group Z^n",
    "H_3: A is an n x n matrix with integer entries",
    "H_4: The determinant of A is non-zero",
    "¬Q: The index of H in G is not finite or not equal to the absolute value of the determinant of A"
]

N_HYP = 4
NEG_Q_INDEX = 4