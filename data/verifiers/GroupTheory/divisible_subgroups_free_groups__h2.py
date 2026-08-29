import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        else:
            F, H = witness
    except Exception:
        return [False, False]

    # H_1: F is a free group
    h1_ok = False
    try:
        from sympy.combinatorics import FreeGroup
        if isinstance(F, FreeGroup):
            h1_ok = True
        else:
            try:
                from sympy.combinatorics.fp_groups import FpGroup
                if isinstance(F, FpGroup) and len(F.relators) == 0:
                    h1_ok = True
            except Exception:
                pass
    except Exception:
        pass

    # neg_Q: H is not the trivial group
    neg_q = False
    try:
        from sympy.combinatorics import FreeGroup
        if isinstance(H, FreeGroup):
            neg_q = (H.rank > 0)
        else:
            try:
                from sympy.combinatorics.fp_groups import FpGroup
                if isinstance(H, FpGroup):
                    neg_q = (H.order() > 1)
                elif hasattr(H, 'order'):
                    o = H.order() if callable(H.order) else H.order
                    neg_q = (o > 1)
                elif hasattr(H, 'generators'):
                    gens = H.generators() if callable(H.generators) else H.generators
                    neg_q = any(not g.is_identity for g in gens)
                elif isinstance(H, (list, tuple, set)):
                    if len(H) == 0:
                        neg_q = False
                    else:
                        neg_q = False
                        for g in H:
                            if hasattr(g, 'is_identity'):
                                if not g.is_identity:
                                    neg_q = True
                                    break
                            elif g != 1:
                                neg_q = True
                                break
                elif hasattr(H, 'is_identity'):
                    neg_q = not H.is_identity
            except Exception:
                pass
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: H is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1