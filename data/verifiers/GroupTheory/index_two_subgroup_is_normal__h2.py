import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: The index of H in G is exactly 2
    try:
        if isinstance(H, PermutationGroup):
            h_elems = list(H.generate_dimino())
        else:
            h_elems = list(set(H))
            
        h_order = len(h_elems)
        is_subset = all(h in G for h in h_elems)
        
        h2_ok = bool(is_subset and G.order() == 2 * h_order)
    except Exception:
        h2_ok = False
        
    # neg_Q: H is NOT a normal subgroup of G
    try:
        if isinstance(H, PermutationGroup):
            h_elems = list(H.generate_dimino())
        else:
            h_elems = list(set(H))
            
        if not h_elems:
            is_normal_subgroup = False
        else:
            id_el = G.identity
            if id_el not in h_elems:
                is_normal_subgroup = False
            else:
                closed = True
                for a in h_elems:
                    for b in h_elems:
                        if (a * b) not in h_elems:
                            closed = False
                            break
                    if not closed:
                        break
                
                if not closed:
                    is_normal_subgroup = False
                else:
                    inverses = True
                    for a in h_elems:
                        if (a**-1) not in h_elems:
                            inverses = False
                            break
                    
                    if not inverses:
                        is_normal_subgroup = False
                    else:
                        normal = True
                        for h in h_elems:
                            for g in list(G.generate_dimino()):
                                if (g * h * g**-1) not in h_elems:
                                    normal = False
                                    break
                            if not normal:
                                break
                        is_normal_subgroup = normal
        neg_q_ok = not is_normal_subgroup
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is exactly 2",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2