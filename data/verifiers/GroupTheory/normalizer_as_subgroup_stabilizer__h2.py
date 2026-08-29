import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
    # The witness is expected to be a tuple (G, H) where G is a group and H is a subset/element.
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: G acts on the set of all subgroups of G by conjugation
    # This is a universal mathematical property for any valid group G.
    try:
        h2_ok = h1_ok
    except Exception:
        h2_ok = False
        
    # ¬Q: The stabilizer of H under this conjugation action is NOT the normalizer N_G(H).
    # The conjugation action is defined on the set of ALL SUBGROUPS of G.
    # If H is not a subgroup of G, it is not in the domain of this action, 
    # so its stabilizer under this action is undefined, meaning it cannot equal N_G(H).
    # If H is a subgroup, its stabilizer under this action is exactly N_G(H), so the conclusion holds.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            try:
                if isinstance(H, PermutationGroup):
                    h_elems = set(H.generate())
                else:
                    h_elems = set(H)
                    
                # Check if H is a subset of G
                is_subset = all(e in G for e in h_elems)
                
                if not is_subset:
                    is_subgrp = False
                else:
                    is_subgrp = True
                    # Check subgroup properties: identity, inverses, and closure
                    if G.identity not in h_elems:
                        is_subgrp = False
                    else:
                        for a in h_elems:
                            if a**-1 not in h_elems:
                                is_subgrp = False
                                break
                            for b in h_elems:
                                if a * b not in h_elems:
                                    is_subgrp = False
                                    break
            except Exception:
                # If any operation fails (e.g., invalid elements), H is not a valid subgroup
                is_subgrp = False
                
            neg_q_ok = not is_subgrp
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on the set of all subgroups of G by conjugation",
    "¬Q: The stabilizer of H under this conjugation action is not the normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2