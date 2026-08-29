import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def get_order(grp):
    if callable(grp.order):
        return grp.order()
    return grp.order

def conditions(witness):
    try:
        G, M = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a nilpotent group
    try:
        nilp = G.is_nilpotent
        if callable(nilp):
            h1 = bool(nilp())
        else:
            h1 = bool(nilp)
    except Exception:
        h1 = False
        
    # H2: M is a maximal subgroup of G
    try:
        h2 = False
        is_sub = M.is_subgroup(G)
        if callable(is_sub):
            is_sub = is_sub()
            
        if is_sub:
            order_G = get_order(G)
            order_M = get_order(M)
            if order_M < order_G:
                is_max = True
                try:
                    reps = G.coset_transversal(M)
                except Exception:
                    reps = list(G.elements)
                
                for g in reps:
                    if g not in M:
                        gens = list(M.generators) + [g]
                        H = PermutationGroup(gens)
                        if get_order(H) < order_G:
                            is_max = False
                            break
                h2 = is_max
    except Exception:
        h2 = False
        
    # neg_Q: M is NOT a normal subgroup of G
    try:
        norm = M.is_normal(G)
        if callable(norm):
            neg_q = not bool(norm())
        else:
            neg_q = not bool(norm)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: M is a maximal subgroup of G",
    "¬Q: M is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2