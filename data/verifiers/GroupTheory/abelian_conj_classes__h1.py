import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        # Evaluate LHS: G is an abelian group
        lhs = bool(witness.is_abelian)
        
        # Evaluate RHS: every conjugacy class of G has exactly one element
        classes = witness.conjugacy_classes()
        rhs = True
        for c in classes:
            if hasattr(c, '__len__'):
                size = len(c)
            elif hasattr(c, 'size'):
                size = c.size
            else:
                size = len(list(c))
                
            if size != 1:
                rhs = False
                break
                
        # Conclusion Q: LHS if and only if RHS
        q = (lhs == rhs)
        
        # Negated conclusion
        neg_q = not q
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not the case that G is an abelian group if and only if every conjugacy class of G has exactly one element"
]

N_HYP = 0
NEG_Q_INDEX = 0