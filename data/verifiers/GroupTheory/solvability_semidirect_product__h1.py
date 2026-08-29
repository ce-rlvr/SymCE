import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        N, H, phi = witness
    except Exception:
        return [False, False]

    # Check H1: phi is a group homomorphism from H to Aut(N)
    h1_ok = False
    try:
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda h, x: phi[h][x]

        N_elems = list(N.generate())
        H_elems = list(H.generate())
        N_elems_set = set(N_elems)
        
        is_hom = True
        for h in H_elems:
            mapped_N = set()
            for x in N_elems:
                px = phi_func(h, x)
                if px not in N_elems_set:
                    is_hom = False
                    break
                mapped_N.add(px)
                for y in N_elems:
                    if phi_func(h, x * y) != px * phi_func(h, y):
                        is_hom = False
                        break
                if not is_hom:
                    break
            if not is_hom:
                break
            if len(mapped_N) != len(N_elems):
                is_hom = False
                break
                
        if is_hom:
            for h1 in H_elems:
                for h2 in H_elems:
                    h1h2 = h1 * h2
                    for x in N_elems:
                        if phi_func(h1h2, x) != phi_func(h1, phi_func(h2, x)):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if not is_hom:
                    break
        h1_ok = is_hom
    except Exception:
        h1_ok = False

    # Check neg_Q: The semidirect product is solvable XOR both N and H are solvable
    neg_q = False
    try:
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda h, x: phi[h][x]

        N_elems = list(N.generate())
        H_elems = list(H.generate())
        
        N_idx = {x: i for i, x in enumerate(N_elems)}
        H_idx = {y: i + len(N_elems) for i, y in enumerate(H_elems)}
        
        gens = []
        
        # Generators from N
        for n in N.generators:
            perm = [0] * (len(N_elems) + len(H_elems))
            for x in N_elems:
                perm[N_idx[x]] = N_idx[x * n]
            for y in H_elems:
                perm[H_idx[y]] = H_idx[y]
            gens.append(Permutation(perm))
            
        # Generators from H
        for h in H.generators:
            perm = [0] * (len(N_elems) + len(H_elems))
            h_inv = ~h
            for x in N_elems:
                perm[N_idx[x]] = N_idx[phi_func(h_inv, x)]
            for y in H_elems:
                perm[H_idx[y]] = H_idx[y * h]
            gens.append(Permutation(perm))
            
        if not gens:
            gens.append(Permutation([i for i in range(len(N_elems) + len(H_elems))]))
            
        G = PermutationGroup(gens)
        
        N_solvable = bool(N.is_solvable)
        H_solvable = bool(H.is_solvable)
        G_solvable = bool(G.is_solvable)
        
        q = (G_solvable == (N_solvable and H_solvable))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "¬Q: N ⋊_phi H is solvable XOR both N and H are solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1