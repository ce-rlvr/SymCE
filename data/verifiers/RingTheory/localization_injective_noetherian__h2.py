import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_prop(obj, keys, default=False):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj:
                return bool(obj[k])
    else:
        for k in keys:
            if hasattr(obj, k):
                val = getattr(obj, k)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    if isinstance(witness, tuple) and len(witness) == 3:
        R, E, S = witness
        try:
            h1 = get_prop(R, ['is_commutative_ring_with_identity', 'is_commutative_ring', 'is_commutative'])
        except Exception:
            pass
        try:
            h2 = get_prop(E, ['is_injective_module', 'is_injective'])
        except Exception:
            pass
        try:
            h3 = get_prop(S, ['is_multiplicatively_closed', 'is_mult_closed'])
        except Exception:
            pass
        try:
            if hasattr(E, 'localized_is_injective'):
                if callable(E.localized_is_injective):
                    q = E.localized_is_injective(S)
                else:
                    q = E.localized_is_injective
            else:
                q = get_prop(witness, ['localized_is_injective', 'S_inv_E_is_injective', 'localized_module_injective', 'is_localized_injective'], default=True)
            neg_q = not bool(q)
        except Exception:
            pass
    else:
        try:
            h1 = get_prop(witness, ['is_commutative_ring_with_identity', 'R_is_commutative_ring_with_identity', 'R_commutative_with_identity', 'is_commutative_ring', 'R_is_commutative_ring'])
        except Exception:
            pass

        try:
            h2 = get_prop(witness, ['is_injective_module', 'E_is_injective_module', 'E_injective', 'is_injective'])
        except Exception:
            pass

        try:
            h3 = get_prop(witness, ['is_multiplicatively_closed', 'S_is_multiplicatively_closed', 'S_multiplicatively_closed', 'is_mult_closed'])
        except Exception:
            pass

        try:
            q = get_prop(witness, ['localized_is_injective', 'S_inv_E_is_injective', 'localized_module_injective', 'is_localized_injective'], default=True)
            neg_q = not q
        except Exception:
            pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: E is an injective R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}E is not an injective S^{-1}R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3