import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # H_1: The quotient group G/Z(G) is abelian
    # Mathematically, G/Z(G) is abelian if and only if the derived subgroup [G, G] is a subgroup of Z(G).
    try:
        Z = witness.center()
        D = witness.derived_subgroup()
        h1 = all(g in Z for g in D.generators)
    except Exception:
        h1 = False

    # ¬Q: G is NOT a nilpotent group of nilpotency class at most 2
    try:
        is_nilp = witness.is_nilpotent
        if callable(is_nilp):
            is_nilp = is_nilp()
            
        if is_nilp:
            c = witness.nilpotency_class
            if callable(c):
                c = c()
            q = (c <= 2)
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The quotient group G/Z(G) is abelian",
    "¬Q: G is not a nilpotent group of nilpotency class at most 2"
]

N_HYP = 1
NEG_Q_INDEX = 1