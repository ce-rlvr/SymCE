import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo
import math
import itertools
import functools

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

class InfinitelyGeneratedFreeGroup:
    def __str__(self):
        return "F_oo"
    def __repr__(self):
        return "F_oo"

F_oo = InfinitelyGeneratedFreeGroup()

def conditions(witness) -> list[bool]:
    try:
        from sympy import oo
        
        is_free = False
        rank = None
        
        if type(witness).__name__ == 'FreeGroup':
            is_free = True
            rank = len(witness.generators)
        elif witness is oo or type(witness).__name__ == 'InfinitelyGeneratedFreeGroup':
            is_free = True
            rank = oo
        elif isinstance(witness, str) and witness.lower() in ["f_oo", "f_infinity", "infinity", "oo"]:
            is_free = True
            rank = oo
        elif isinstance(witness, int) and not isinstance(witness, bool) and witness >= 0:
            is_free = True
            rank = witness
        elif hasattr(witness, 'order') and callable(getattr(witness, 'order')):
            try:
                if witness.order() == 1:
                    is_free = True
                    rank = 0
            except Exception:
                pass
                
        h1 = is_free
    except Exception:
        h1 = False

    try:
        from sympy import oo
        if rank is not None:
            neg_q = bool(rank == oo)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: Aut(F) is not finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1