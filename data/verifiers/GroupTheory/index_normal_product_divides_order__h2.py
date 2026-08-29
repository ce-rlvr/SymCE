import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, H, N = witness
            HN_provided = None
        elif len(witness) == 4:
            G, H, N, HN_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: HN is the set containing all products hn where h in H and n in N
    try:
        if isinstance(H, PermutationGroup):
            H_elems = list(H.elements)
        else:
            H_elems = list(set(H))
            
        h3_valid_H = all(h in G for h in H_elems)
        
        N_elems = list(N.elements)
        
        HN_computed = set()
        for h in H_elems:
            for n in N_elems:
                HN_computed.add(h * n)
                
        if HN_provided is not None:
            if isinstance(HN_provided, PermutationGroup):
                HN_prov_elems = set(HN_provided.elements)
            else:
                HN_prov_elems = set(HN_provided)
            h3 = h3_valid_H and (HN_computed == HN_prov_elems)
        else:
            h3 = h3_valid_H
    except Exception:
        h3 = False
        
    # neg_Q: The index of N in HN does not divide the order of H
    try:
        N_order = len(list(N.elements))
        HN_order = len(HN_computed)
        if HN_order % N_order != 0:
            neg_q = False
        else:
            index = HN_order // N_order
            H_order = len(H_elems)
            neg_q = (H_order % index != 0)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: HN is the set containing all products hn where h in H and n in N",
    "¬Q: The index of N in HN does not divide the order of H"
]

N_HYP = 3
NEG_Q_INDEX = 3