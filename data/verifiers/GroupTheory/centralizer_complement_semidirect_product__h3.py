import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        if G.order() > 2000:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G is an internal semidirect product of N and H
    try:
        n_sub = all(G.contains(g) for g in N.generators)
        h_sub = all(G.contains(g) for g in H.generators)
        
        n_normal = True
        if n_sub:
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * g**-1):
                        n_normal = False
                        break
                if not n_normal:
                    break
        else:
            n_normal = False
            
        N_elements = list(N.generate())
        H_elements = list(H.generate())
        
        intersection_trivial = True
        for n in N_elements:
            if n == n**2:  # Identity check
                continue
            if n in H_elements:
                intersection_trivial = False
                break
                
        product_correct = (len(N_elements) * len(H_elements) == G.order())
        
        h1_ok = bool(n_sub and h_sub and n_normal and intersection_trivial and product_correct)
    except Exception:
        h1_ok = False

    # ¬Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)
    try:
        G_elements = list(G.generate())
        h_gens = H.generators
        
        C_G_H = []
        for g in G_elements:
            if all(g * h == h * g for h in h_gens):
                C_G_H.append(g)
                
        C_N_H = []
        for n in N_elements:
            if all(n * h == h * n for h in h_gens):
                C_N_H.append(n)
                
        Z_H = []
        for h in H_elements:
            if all(h * x == x * h for x in h_gens):
                Z_H.append(h)
                
        size_matches = (len(C_G_H) == len(C_N_H) * len(Z_H))
        
        commute = True
        for n in C_N_H:
            for z in Z_H:
                if n * z != z * n:
                    commute = False
                    break
            if not commute:
                break
                
        intersection_trivial_CZ = True
        for n in C_N_H:
            if n == n**2:  # Identity check
                continue
            if n in Z_H:
                intersection_trivial_CZ = False
                break
                
        q_ok = size_matches and commute and intersection_trivial_CZ
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an internal semidirect product of a normal subgroup N and a subgroup H",
    "¬Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1