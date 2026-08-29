import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    h1 = False
    neg_q = False
    
    # 1. Mock object with properties
    try:
        if hasattr(witness, 'is_finite_galois_extension'):
            h1 = bool(witness.is_finite_galois_extension)
            if hasattr(witness, 'K_G_equals_F'):
                neg_q = not bool(witness.K_G_equals_F)
            elif hasattr(witness, 'fixed_field') and hasattr(witness, 'base_field'):
                neg_q = witness.fixed_field != witness.base_field
            else:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 2. Dictionary representation
    try:
        if isinstance(witness, dict):
            if 'is_finite_galois_extension' in witness:
                h1 = bool(witness['is_finite_galois_extension'])
                if 'K_G_equals_F' in witness:
                    neg_q = not bool(witness['K_G_equals_F'])
                elif 'fixed_field' in witness and 'base_field' in witness:
                    neg_q = witness['fixed_field'] != witness['base_field']
                else:
                    neg_q = True
                return [h1, neg_q]
    except Exception:
        pass

    # 3. Tuple of 2 groups (G, H) or (H, G)
    # By Galois correspondence, H represents Gal(K/F) and G represents the entire Galois group.
    # K/F is a finite Galois extension iff H is a finite group (always true for sympy PermutationGroups).
    # K^G == F iff G == H.
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, B = witness
            if hasattr(A, 'is_group') and hasattr(B, 'is_group'):
                a_sub_b = False
                b_sub_a = False
                try:
                    a_sub_b = A.is_subgroup(B)
                except Exception:
                    pass
                try:
                    b_sub_a = B.is_subgroup(A)
                except Exception:
                    pass
                
                if a_sub_b:
                    H, G = A, B
                    h1 = True
                elif b_sub_a:
                    H, G = B, A
                    h1 = True
                else:
                    h1 = False
                
                if h1:
                    neg_q = (H.order() != G.order())
                return [h1, neg_q]
    except Exception:
        pass

    # 4. Tuple of 3 mock objects (K, F, G)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            K, F, G = witness
            if hasattr(K, 'is_finite_galois_extension'):
                h1 = bool(K.is_finite_galois_extension(F))
                neg_q = K.fixed_field(G) != F
                return [h1, neg_q]
    except Exception:
        pass

    # 5. Tuple of integers (order_H, order_G)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, B = witness
            if isinstance(A, int) and isinstance(B, int):
                if A > 0 and B > 0:
                    if B % A == 0:
                        h1 = True
                        neg_q = (A != B)
                        return [h1, neg_q]
    except Exception:
        pass

    # 6. Single group G (assuming F = K, so H is trivial)
    try:
        if hasattr(witness, 'is_group') and witness.is_group:
            h1 = True
            neg_q = witness.order() > 1
            return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "¬Q: The fixed field of K under the action of G is not exactly the base field F"
]

N_HYP = 1
NEG_Q_INDEX = 1