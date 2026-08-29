import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = H.is_subgroup(G)
        else:
            h1 = all(G.contains(g) for g in H.generators)
    except Exception:
        h1 = False
        
    try:
        if hasattr(N, 'is_subgroup'):
            n_sub = N.is_subgroup(G)
        else:
            n_sub = all(G.contains(g) for g in N.generators)
        h2 = n_sub and N.is_normal(G)
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        for h in H.generate():
            for n in N.generate():
                comm = h * n * (~h) * (~n)
                if not N.contains(comm):
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and N is not a subgroup of N"
]

N_HYP = 2
NEG_Q_INDEX = 2