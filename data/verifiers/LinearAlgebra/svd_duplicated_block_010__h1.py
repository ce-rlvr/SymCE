import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.matrices import eye, zeros
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, B = witness
        else:
            A = witness
            B = A.row_join(A) if hasattr(A, 'row_join') else None
    except Exception:
        A = None
        B = None

    h1_ok = False
    try:
        if A is not None and B is not None and hasattr(A, 'row_join'):
            h1_ok = bool(B == A.row_join(A))
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        if A is not None and B is not None and hasattr(A, 'singular_values') and hasattr(B, 'singular_values'):
            sv_A = A.singular_values()
            sv_B = B.singular_values()
            
            expected_sv_B = [sympy.sqrt(2) * s for s in sv_A]
            
            if len(expected_sv_B) != len(sv_B):
                neg_q = True
            else:
                try:
                    expected_sv_B_sorted = sorted([float(s.evalf()) for s in expected_sv_B])
                    sv_B_sorted = sorted([float(s.evalf()) for s in sv_B])
                    is_equal = True
                    for e1, e2 in zip(expected_sv_B_sorted, sv_B_sorted):
                        if abs(e1 - e2) > 1e-9:
                            is_equal = False
                            break
                    neg_q = not is_equal
                except Exception:
                    l2 = list(sv_B)
                    is_equal = True
                    for e1 in expected_sv_B:
                        found = False
                        for i, e2 in enumerate(l2):
                            try:
                                if sympy.simplify(e1 - e2) == 0:
                                    l2.pop(i)
                                    found = True
                                    break
                            except Exception:
                                pass
                        if not found:
                            is_equal = False
                            break
                    neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: B is the block matrix A concatenated with A",
    "¬Q: The singular values of B are not exactly sqrt(2) times the singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1