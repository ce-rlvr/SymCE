import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

try:
    from sympy.combinatorics import free_group, FreeGroup
except ImportError:
    pass

# Top-level setup: named object bindings
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
    "H_1: F is a free group",
    "¬Q: H is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        else:
            F, H = witness
    except Exception:
        return [False, False]

    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
        if not h1:
            try:
                from sympy.combinatorics import FreeGroup as FG
                h1 = isinstance(F, FG)
            except ImportError:
                pass
    except Exception:
        h1 = False

    # neg_Q: H is not the trivial subgroup
    try:
        is_trivial = False
        if isinstance(H, (list, tuple, set)):
            if not H:
                is_trivial = True
            else:
                if hasattr(F, 'identity'):
                    is_trivial = all(h == F.identity for h in H)
                else:
                    is_trivial = all(h == 1 for h in H)
        elif hasattr(H, 'is_trivial'):
            if callable(H.is_trivial):
                is_trivial = H.is_trivial()
            else:
                is_trivial = H.is_trivial
        elif hasattr(H, 'order'):
            if callable(H.order):
                try:
                    is_trivial = (H.order() == 1)
                except Exception:
                    is_trivial = False
            else:
                is_trivial = (H.order == 1)
        elif hasattr(H, 'generators'):
            if not H.generators:
                is_trivial = True
            elif hasattr(F, 'identity'):
                is_trivial = all(g == F.identity for g in H.generators)
            else:
                is_trivial = False
        else:
            if hasattr(F, 'identity'):
                is_trivial = (H == F.identity)
            else:
                is_trivial = (H == 1)
        
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]