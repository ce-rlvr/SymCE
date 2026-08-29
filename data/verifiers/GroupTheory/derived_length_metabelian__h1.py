import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        # H_1: Assume G is a metabelian group
        # A group is metabelian if its second derived subgroup is trivial.
        G2 = witness.derived_subgroup().derived_subgroup()
        h1 = bool(G2.is_trivial)
    except Exception:
        h1 = False

    try:
        # Conclusion: The derived length of G is at most 2, and the second derived subgroup G^{(2)} is the trivial subgroup.
        ds = witness.derived_series()
        if ds[-1].is_trivial:
            dl = len(ds) - 1
        else:
            dl = float('inf')
        
        G2 = witness.derived_subgroup().derived_subgroup()
        
        q = (dl <= 2) and bool(G2.is_trivial)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a metabelian group",
    "¬Q: The derived length of G is greater than 2, or the second derived subgroup G^{(2)} is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1