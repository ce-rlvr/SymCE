import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    def get_elements(group):
        try:
            return list(group.elements)
        except Exception:
            try:
                return list(group.generate())
            except Exception:
                return list(group)

    # H_1: H is a subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            h1 = False
        else:
            try:
                h1 = H.is_subgroup(G)
            except Exception:
                h1 = all(h in G for h in H.generators)
    except Exception:
        h1 = False

    # H_2: K is a subgroup of G
    try:
        if not isinstance(K, PermutationGroup):
            h2 = False
        else:
            try:
                h2 = K.is_subgroup(G)
            except Exception:
                h2 = all(k in G for k in K.generators)
    except Exception:
        h2 = False

    # neg_Q: The order of the product HK is not equal to lcm(|H|, |K|)
    try:
        H_elems = set(get_elements(H))
        K_elems = set(get_elements(K))
        
        HK_set = set(h * k for h in H_elems for k in K_elems)
        HK_order = len(HK_set)
        
        H_order = len(H_elems)
        K_order = len(K_elems)
        
        lcm_HK = (H_order * K_order) // math.gcd(H_order, K_order)
        
        neg_q = (HK_order != lcm_HK)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "¬Q: The order of the product HK is not equal to lcm(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2