import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # Wait, V4 is not A4. V4 is a subgroup of A4.
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: G is the internal semidirect product of N and H
    try:
        h3 = H.is_subgroup(G) and N.intersect(H).is_trivial and G.order() == N.order() * H.order()
    except Exception:
        h3 = False
        
    # Conclusion: N_G(H) is the internal semidirect product of C_N(H) and H
    try:
        gens_H = H.generators
        
        norm_elems = []
        for g in G.elements:
            if all(H.contains(g * h * ~g) for h in gens_H):
                norm_elems.append(g)
        N_G_H = PermutationGroup(norm_elems)
        
        cent_elems = []
        for n in N.elements:
            if all(n * h == h * n for h in gens_H):
                cent_elems.append(n)
        C_N_H = PermutationGroup(cent_elems)
        
        cond1 = C_N_H.is_subgroup(N_G_H) and C_N_H.is_normal(N_G_H)
        cond2 = H.is_subgroup(N_G_H)
        cond3 = C_N_H.intersect(H).is_trivial
        cond4 = N_G_H.order() == C_N_H.order() * H.order()
        
        q = cond1 and cond2 and cond3 and cond4
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: N_G(H) is not the internal semidirect product of C_N(H) and H"
]

N_HYP = 3
NEG_Q_INDEX = 3