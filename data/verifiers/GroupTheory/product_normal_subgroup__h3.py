import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The set product HN is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if h1 and isinstance(N, PermutationGroup):
            is_sub = True
            for n in N.generators:
                try:
                    if n not in G:
                        is_sub = False
                        break
                except Exception:
                    is_sub = False
                    break
            
            is_norm = True
            if is_sub:
                for g in G.generators:
                    for n in N.generators:
                        try:
                            if (g * n * ~g) not in N:
                                is_norm = False
                                break
                        except Exception:
                            is_norm = False
                            break
                    if not is_norm:
                        break
            h2 = is_sub and is_norm
    except Exception:
        h2 = False

    # neg_Q: HN is NOT a subgroup of G
    try:
        neg_q = False
        if h1 and isinstance(N, PermutationGroup):
            try:
                if hasattr(H, 'generate'):
                    H_elements = list(H.generate())
                else:
                    H_elements = list(H)
            except Exception:
                H_elements = []
                
            N_elements = list(N.generate())
            HN = set()
            valid_elements = True
            for h in H_elements:
                for n in N_elements:
                    try:
                        HN.add(h * n)
                    except Exception:
                        valid_elements = False
                        break
                if not valid_elements:
                    break
            
            if not valid_elements:
                is_subgroup = False
            else:
                is_subgroup = True
                if not HN:
                    is_subgroup = False
                else:
                    for x in HN:
                        try:
                            if x not in G:
                                is_subgroup = False
                                break
                        except Exception:
                            is_subgroup = False
                            break
                    
                    if is_subgroup:
                        for a in HN:
                            for b in HN:
                                try:
                                    if (a * b) not in HN:
                                        is_subgroup = False
                                        break
                                except Exception:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                    
                    if is_subgroup:
                        for a in HN:
                            try:
                                if (~a) not in HN:
                                    is_subgroup = False
                                    break
                            except Exception:
                                is_subgroup = False
                                break
            
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]