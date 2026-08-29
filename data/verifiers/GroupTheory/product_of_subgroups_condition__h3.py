import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def _get_elements(obj):
    if hasattr(obj, 'generate'):
        return set(obj.generate())
    elif hasattr(obj, 'elements'):
        return set(obj.elements)
    else:
        return set(obj)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        G_elems = _get_elements(G)
        H_elems = _get_elements(H)
        
        if not H_elems or not H_elems.issubset(G_elems):
            h2 = False
        else:
            h2 = True
            for a in H_elems:
                if ~a not in H_elems:
                    h2 = False
                    break
                for b in H_elems:
                    if a * b not in H_elems:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # neg_Q: HK is a subgroup of G iff HK = KH
    try:
        G_elems = _get_elements(G)
        H_elems = _get_elements(H)
        K_elems = _get_elements(K)
        
        HK = set(h * k for h in H_elems for k in K_elems)
        KH = set(k * h for k in K_elems for h in H_elems)
        
        hk_equals_kh = (HK == KH)
        
        if not HK or not HK.issubset(G_elems):
            hk_is_subgroup = False
        else:
            hk_is_subgroup = True
            for a in HK:
                if ~a not in HK:
                    hk_is_subgroup = False
                    break
                for b in HK:
                    if a * b not in HK:
                        hk_is_subgroup = False
                        break
                        
        neg_q = (hk_is_subgroup != hk_equals_kh)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: (HK is a subgroup of G) is not equivalent to (HK = KH)"
]

N_HYP = 2
NEG_Q_INDEX = 2