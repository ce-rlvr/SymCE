import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
            
        if isinstance(G, FreeGroup):
            h1 = True
        elif isinstance(G, FpGroup):
            h1 = len(G.relators) == 0
        elif hasattr(G, 'is_free_group'):
            val = G.is_free_group
            h1 = bool(val()) if callable(val) else bool(val)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
            
        if hasattr(G, 'has_solvable_word_problem'):
            val = G.has_solvable_word_problem
            neg_q = not (bool(val()) if callable(val) else bool(val))
        else:
            # The word problem for any free group is solvable via free reduction.
            # Since SymPy only constructs finitely generated free groups (or finitely presented groups),
            # and we cannot compute undecidability for arbitrary FpGroups, we return False.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: The word problem for F is unsolvable"
]

N_HYP = 1
NEG_Q_INDEX = 1