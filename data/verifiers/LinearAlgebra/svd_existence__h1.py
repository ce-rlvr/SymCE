import sympy
from sympy import Matrix, Expr, simplify
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    def has_svd(A):
        try:
            M = Matrix(A)
        except Exception:
            return False
            
        try:
            M = simplify(M)
        except Exception:
            pass
            
        if M.rows == 0 or M.cols == 0:
            return True
            
        is_complex_numeric = True
        for e in M:
            if not isinstance(e, Expr):
                is_complex_numeric = False
                break
            if not e.is_number:
                is_complex_numeric = False
                break
            if not e.is_finite:
                is_complex_numeric = False
                break
            try:
                complex(e)
            except TypeError:
                is_complex_numeric = False
                break

        if is_complex_numeric:
            return True
            
        try:
            svs = M.singular_values()
            if all(isinstance(sv, Expr) and sv.is_number and sv.is_real and sv >= 0 for sv in svs):
                return True
        except Exception:
            pass
            
        return False

    try:
        neg_q = not has_svd(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A does not have a Singular Value Decomposition over C"
]

N_HYP = 0
NEG_Q_INDEX = 0