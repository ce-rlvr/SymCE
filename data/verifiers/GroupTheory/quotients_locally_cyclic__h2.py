import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import primefactors

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

def is_cyclic_group(G):
    if hasattr(G, 'is_cyclic'):
        val = G.is_cyclic
        if callable(val):
            return bool(val())
        elif val is not None:
            return bool(val)
    order = G.order()
    for g in G.elements:
        if g.order() == order:
            return True
    return False

def is_normal_subgroup(G, N):
    if hasattr(G, 'is_normal'):
        try:
            return G.is_normal(N)
        except Exception:
            pass
    for g in G.generators:
        for n in N.generators:
            if (g * n * (~g)) not in N:
                return False
    return True

def is_quotient_cyclic(G, N):
    target_order = G.order() // N.order()
    if target_order == 1:
        return True
        
    factors = primefactors(target_order)
    
    for g in G.elements:
        is_gen = True
        for p in factors:
            k = target_order // p
            if (g**k) in N:
                is_gen = False
                break
        if is_gen:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H1: G is a locally cyclic group
    try:
        h1 = is_cyclic_group(G)
    except Exception:
        h1 = False
        
    # neg_Q: G/N is NOT a locally cyclic group
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = True
        elif not N.is_subgroup(G):
            neg_q = True
        elif not is_normal_subgroup(G, N):
            neg_q = True
        else:
            neg_q = not is_quotient_cyclic(G, N)
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a locally cyclic group",
    "¬Q: The quotient group G/N is not a locally cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1