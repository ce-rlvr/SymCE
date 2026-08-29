import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(G):
    try:
        return list(G.generate())
    except Exception:
        return list(G.elements)

def get_identity(G):
    try:
        return G.identity
    except Exception:
        for g in get_elements(G):
            return g**0

def is_nilpotent(H):
    try:
        if hasattr(H, 'is_nilpotent'):
            val = H.is_nilpotent
            if callable(val):
                return val()
            return val
    except Exception:
        pass
    
    try:
        lcs = H.lower_central_series()
        return lcs[-1].order() == 1
    except Exception:
        pass
        
    return False

def fitting_subgroup(G):
    gens = []
    for H in G.normal_subgroups():
        if is_nilpotent(H):
            gens.extend(H.generators)
    if not gens:
        return PermutationGroup([get_identity(G)])
    return PermutationGroup(gens)

def centralizer(G, H):
    h_gens = H.generators
    cent_gens = []
    for g in get_elements(G):
        if all(g * h == h * g for h in h_gens):
            cent_gens.append(g)
    if not cent_gens:
        return PermutationGroup([get_identity(G)])
    return PermutationGroup(cent_gens)

def is_subgroup(A, B):
    for g in A.generators:
        try:
            if not B.contains(g):
                return False
        except Exception:
            if g not in B:
                return False
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            F = fitting_subgroup(witness)
            C = centralizer(witness, F)
            neg_q = not is_subgroup(C, F)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a valid permutation group",
    "¬Q: The centralizer of F(G) in G is not a subgroup of F(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1