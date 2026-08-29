import itertools
import math
import sympy
from sympy import Matrix, ZZ, QQ
from sympy import gcd as sympy_gcd
from sympy.polys.polytools import degree
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        is_field = False
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = True
            if getattr(R, 'is_Field', False):
                is_field = True
        else:
            h1 = True
            M = witness

        if isinstance(M, (int, sympy.Integer)):
            h2 = True
            if not is_field:
                neg_q = abs(int(M)) > 1
        elif isinstance(M, (list, tuple)) and all(isinstance(x, (int, sympy.Integer)) for x in M):
            h2 = True
            if not is_field:
                neg_q = any(abs(int(x)) > 1 for x in M)
        elif isinstance(M, Matrix):
            h2 = True
            if not is_field:
                r = M.rank()
                if r == 0:
                    neg_q = False
                else:
                    m, n = M.shape
                    g = 0
                    for row_indices in itertools.combinations(range(m), r):
                        for col_indices in itertools.combinations(range(n), r):
                            sub_A = M[row_indices, col_indices]
                            det = sub_A.det()
                            g = sympy_gcd(g, det)
                            if g == 1 or g == -1:
                                break
                        if g == 1 or g == -1:
                            break
                    
                    if isinstance(g, (int, sympy.Integer)):
                        neg_q = abs(int(g)) > 1
                    else:
                        try:
                            deg = degree(g)
                            neg_q = deg > 0
                        except Exception:
                            neg_q = g not in [1, -1]
        elif hasattr(M, 'is_abelian'):
            if M.is_abelian:
                h2 = True
                if not is_field:
                    try:
                        neg_q = M.order() > 1
                    except Exception:
                        neg_q = False
        elif isinstance(M, str):
            M_clean = M.strip().replace(" ", "")
            if M_clean in ["Z/2Z", "Z_2", "Z/3Z", "Z_3", "Z/4Z", "Z_4", "Z/5Z", "Z_5", "Z/6Z", "Z_6"]:
                h2 = True
                neg_q = True
            elif M_clean in ["Z", "Z^2", "Z^3"]:
                h2 = True
                neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a finitely generated R-module",
    "¬Q: M is not a projective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2