import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    H3 = False
    neg_Q = False
    
    try:
        if isinstance(witness, dict):
            H1 = bool(witness.get('H1', witness.get('R_is_commutative_ring_with_identity', False)))
            H2 = bool(witness.get('H2', witness.get('M_is_finitely_presented', False)))
            H3 = bool(witness.get('H3', witness.get('N_is_module', False)))
            is_iso = witness.get('Q', witness.get('canonical_map_is_isomorphism', True))
            neg_Q = not bool(is_iso)
        else:
            H1 = bool(getattr(witness, 'H1', getattr(witness, 'R_is_commutative_ring_with_identity', False)))
            H2 = bool(getattr(witness, 'H2', getattr(witness, 'M_is_finitely_presented', False)))
            H3 = bool(getattr(witness, 'H3', getattr(witness, 'N_is_module', False)))
            is_iso = getattr(witness, 'Q', getattr(witness, 'canonical_map_is_isomorphism', True))
            neg_Q = not bool(is_iso)
    except Exception:
        pass

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a finitely presented R-module",
    "H_3: N is an R-module",
    "¬Q: The canonical S^{-1}R-module homomorphism is NOT an isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3