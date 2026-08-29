import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a normal subgroup of G
    try:
        h1 = True
        for h in H.generators:
            if h not in G:
                h1 = False
                break
        if h1:
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: K is a normal subgroup of G
    try:
        h2 = True
        for k in K.generators:
            if k not in G:
                h2 = False
                break
        if h2:
            for g in G.generators:
                for k in K.generators:
                    if (g * k * ~g) not in K:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: The product HK is NOT a normal subgroup of G
    try:
        def get_elements(grp):
            if hasattr(grp, 'elements'):
                return set(grp.elements)
            return set(grp.generate())
        
        H_elems = get_elements(H)
        K_elems = get_elements(K)
        HK_elems = {h * k for h in H_elems for k in K_elems}
        
        is_subgroup = True
        if not HK_elems:
            is_subgroup = False
        else:
            for x in HK_elems:
                for y in HK_elems:
                    if (x * ~y) not in HK_elems:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
        
        is_normal = True
        if is_subgroup:
            for g in G.generators:
                for x in HK_elems:
                    if (g * x * ~g) not in HK_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
        
        neg_q = not (is_subgroup and is_normal)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: K is a normal subgroup of G",
    "¬Q: The product HK is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2