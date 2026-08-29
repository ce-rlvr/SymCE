import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, N, H = witness
        else:
            G = witness
            N, H = None, None
            
            # Auto-discover N and H if only G is provided
            try:
                N_cands = [G.derived_subgroup()]
                for N_cand in N_cands:
                    if N_cand.order() == G.order():
                        continue
                    target_H_order = G.order() // N_cand.order()
                    for g in G.generate():
                        if g.order() == target_H_order:
                            H_cand = PermutationGroup([g])
                            if H_cand.is_abelian:
                                normal_ok = True
                                for gen_g in G.generators:
                                    for n in N_cand.generators:
                                        if not N_cand.contains(~gen_g * n * gen_g):
                                            normal_ok = False
                                            break
                                    if not normal_ok:
                                        break
                                if normal_ok:
                                    N = N_cand
                                    H = H_cand
                                    break
                    if N is not None:
                        break
            except Exception:
                pass

    except Exception:
        return [False, False, False]

    if N is None or H is None:
        return [False, False, False]

    # H1: H is an abelian group
    try:
        h1 = bool(H.is_abelian)
    except Exception:
        h1 = False

    # H2: G is an external semidirect product of N and H
    try:
        normal_ok = True
        for g in G.generators:
            for n in N.generators:
                n_val = n
                g_val = g
                if hasattr(n, 'size') and hasattr(g, 'size') and n.size != g.size:
                    max_size = max(n.size, g.size)
                    n_val = Permutation(n, size=max_size)
                    g_val = Permutation(g, size=max_size)
                
                conj = ~g_val * n_val * g_val
                
                if hasattr(conj, 'size') and hasattr(N, 'degree') and conj.size != N.degree:
                    conj = Permutation(conj, size=N.degree)
                    
                if not N.contains(conj):
                    normal_ok = False
                    break
            if not normal_ok:
                break
        
        sub_ok = True
        for h in H.generators:
            h_val = h
            if hasattr(h, 'size') and hasattr(G, 'degree') and h.size != G.degree:
                h_val = Permutation(h, size=G.degree)
            if not G.contains(h_val):
                sub_ok = False
                break
                
        size_ok = (G.order() == N.order() * H.order())
        
        h2 = bool(normal_ok and sub_ok and size_ok)
    except Exception:
        h2 = False

    # neg_Q: G is NOT a metabelian group
    try:
        D = G.derived_subgroup()
        neg_q = not bool(D.is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is an abelian group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2