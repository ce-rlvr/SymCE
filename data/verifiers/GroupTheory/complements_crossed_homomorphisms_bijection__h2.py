import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from itertools import product

# Top-level setup for witness expressions
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
        G, N, H = witness
        
        # Allow lists of permutations to be passed as subgroups
        if isinstance(G, list):
            G = PermutationGroup(G)
        if isinstance(N, list):
            N = PermutationGroup(N)
        if isinstance(H, list):
            H = PermutationGroup(H)
            
        id_el = G.generators[0] ** 0 if G.generators else Permutation()
            
        # Hypothesis 1: G = N \rtimes H
        # Check if N and H are subgroups of G
        n_in_g = all(g in G for g in N.generators)
        h_in_g = all(g in G for g in H.generators)
        
        # Check if N is normal in G
        is_normal = True
        for n in N.generators:
            for g in G.generators:
                if (g * n * ~g) not in N:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        # Check if N \cap H = {1}
        H_elements = list(H.generate())
        intersection_trivial = True
        for h in H_elements:
            if h != id_el and h in N:
                intersection_trivial = False
                break
                
        # Check if G = NH (since intersection is trivial, |N|*|H| == |G| is sufficient)
        order_eq = (N.order() * H.order() == G.order())
        
        h1_ok = bool(n_in_g and h_in_g and is_normal and intersection_trivial and order_eq)
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            N_elements = list(N.generate())
            h_gens = H.generators
            
            # Find all complements of N in G
            complements = []
            for n_tuple in product(N_elements, repeat=len(h_gens)):
                k_gens = [n * h for n, h in zip(n_tuple, h_gens)]
                if not k_gens:
                    k_gens = [id_el]
                
                K = PermutationGroup(k_gens)
                
                # A subgroup K is a complement if |K| == |H| and K \cap N = {1}
                if K.order() == H.order():
                    intersect_trivial = True
                    for k in K.generate():
                        if k != id_el and k in N:
                            intersect_trivial = False
                            break
                    if intersect_trivial:
                        complements.append(K)
                        
            # Construct the set of crossed homomorphisms Z^1(H, N)
            # Each complement K corresponds to exactly one crossed homomorphism f: H -> N
            Z1 = []
            for K in complements:
                f = {}
                for k in K.generate():
                    # For each k in K, find the unique h in H such that k * h^-1 is in N
                    for h in H_elements:
                        if (k * ~h) in N:
                            f[h] = k * ~h
                            break
                Z1.append(f)
                
            # Check if Z^1(H, N) forms a group under pointwise multiplication
            is_group = True
            for f in Z1:
                for g in Z1:
                    fg = {}
                    for h in H_elements:
                        fg[h] = f[h] * g[h]
                    
                    # If the pointwise product is not a valid crossed homomorphism, it's not a group
                    if fg not in Z1:
                        is_group = False
                        break
                if not is_group:
                    break
                    
            # The conclusion fails if Z^1(H, N) is not a group
            neg_q = not is_group
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semidirect product of N and H",
    "¬Q: The set of crossed homomorphisms Z^1(H, N) does not form a group under pointwise multiplication"
]

N_HYP = 1
NEG_Q_INDEX = 1