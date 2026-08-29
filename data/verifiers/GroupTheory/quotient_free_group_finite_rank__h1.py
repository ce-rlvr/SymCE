import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for witness expressions
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

# Common infinite groups
Q = sympy.S.Rationals
Z = sympy.S.Integers
R = sympy.S.Reals
C = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is a group
        is_grp = False
        if hasattr(witness, 'generators') and hasattr(witness, 'identity'):
            is_grp = True
        elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            is_grp = True
            
        # Check if witness is finitely generated
        is_fg = False
        if hasattr(witness, 'generators') and hasattr(witness, 'identity'):
            try:
                is_fg = len(witness.generators) < float('inf')
            except Exception:
                is_fg = False
        elif witness == sympy.S.Integers:
            is_fg = True
        elif hasattr(witness, 'is_finite') and witness.is_finite:
            is_fg = True
            
        # The conclusion states that G is finitely generated (there exists a free group of finite rank mapping onto G).
        # The negated conclusion is that G is a group, but NOT finitely generated.
        neg_q = is_grp and not is_fg
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: G is not finitely generated (no free group of finite rank maps onto G)"
]

N_HYP = 0
NEG_Q_INDEX = 0