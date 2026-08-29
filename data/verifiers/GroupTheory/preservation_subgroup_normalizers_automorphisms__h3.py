import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: N_G(H) denotes the normalizer of H in G
    # We verify that phi is a valid map from G to G, as it is required for the conclusion.
    try:
        G_elems = set(G.generate())
        if isinstance(phi, dict):
            h3 = all(g in phi for g in G_elems) and all(phi[g] in G_elems for g in G_elems)
        else:
            h3 = all(phi(g) in G_elems for g in G_elems)
    except Exception:
        h3 = False

    # neg_Q: N_G(\phi(H)) != \phi(N_G(H))
    try:
        G_elems = set(G.generate())
        H_elems = set(H.generate())
        
        if isinstance(phi, dict):
            def eval_phi(x): return phi[x]
        else:
            def eval_phi(x): return phi(x)
            
        phi_H = {eval_phi(h) for h in H_elems}
        
        # Compute N_G(\phi(H))
        N_G_phi_H = set()
        for g in G_elems:
            g_inv = ~g
            conj = {g * x * g_inv for x in phi_H}
            if conj == phi_H:
                N_G_phi_H.add(g)
                
        # Compute N_G(H)
        N_G_H = set()
        for g in G_elems:
            g_inv = ~g
            conj = {g * x * g_inv for x in H_elems}
            if conj == H_elems:
                N_G_H.add(g)
                
        # Compute \phi(N_G(H))
        phi_N_G_H = {eval_phi(x) for x in N_G_H}
        
        neg_q = (N_G_phi_H != phi_N_G_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N_G(H) denotes the normalizer of H in G",
    "¬Q: N_G(\\phi(H)) != \\phi(N_G(H))"
]

N_HYP = 3
NEG_Q_INDEX = 3