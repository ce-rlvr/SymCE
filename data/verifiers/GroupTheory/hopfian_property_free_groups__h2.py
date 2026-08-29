import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
            F, phi = witness
            if isinstance(F, dict) and isinstance(phi, dict):
                h1 = bool(F.get('is_fg_free_group', False))
                h2 = bool(phi.get('is_surjective', False))
                neg_q = not bool(phi.get('is_injective', True))
                return [h1, h2, neg_q]
            if hasattr(F, 'is_fg_free_group') and hasattr(phi, 'is_surjective'):
                h1 = bool(getattr(F, 'is_fg_free_group', False))
                h2 = bool(getattr(phi, 'is_surjective', False))
                neg_q = not bool(getattr(phi, 'is_injective', True))
                return [h1, h2, neg_q]
                
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_fg_free_group', False))
            h2 = bool(witness.get('is_surjective', False))
            neg_q = not bool(witness.get('is_injective', True))
            return [h1, h2, neg_q]
        
        if hasattr(witness, 'is_fg_free_group'):
            h1 = bool(getattr(witness, 'is_fg_free_group', False))
            h2 = bool(getattr(witness, 'is_surjective', False))
            neg_q = not bool(getattr(witness, 'is_injective', True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "H_2: phi is surjective",
    "¬Q: phi is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2