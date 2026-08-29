import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal cyclic subgroup of G
    try:
        h1 = False
        if N.is_subgroup(G):
            # Check if N is normal in G
            is_norm = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * g**-1) not in N:
                        is_norm = False
                        break
                if not is_norm:
                    break
            
            if is_norm:
                # Check if N is cyclic
                is_cyc = False
                n_order = N.order()
                if n_order == 1:
                    is_cyc = True
                else:
                    for n in N.elements:
                        if n.order() == n_order:
                            is_cyc = True
                            break
                h1 = is_cyc
    except Exception:
        h1 = False

    # H_2: The quotient group G/N is a cyclic group
    try:
        h2 = False
        # First verify N is a normal subgroup to ensure G/N is a valid group
        is_norm = False
        if N.is_subgroup(G):
            is_norm = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * g**-1) not in N:
                        is_norm = False
                        break
                if not is_norm:
                    break
                    
        if is_norm:
            target_order = G.order() // N.order()
            for g in G.elements:
                k = 1
                curr = g
                while curr not in N and k <= target_order:
                    curr = curr * g
                    k += 1
                if k == target_order and curr in N:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # ¬Q: The derived subgroup G' is NOT cyclic OR G' is NOT contained in N
    try:
        neg_q = False
        G_prime = G.derived_subgroup()
        
        # Check if G' is cyclic
        gp_order = G_prime.order()
        gp_is_cyc = False
        if gp_order == 1:
            gp_is_cyc = True
        else:
            for x in G_prime.elements:
                if x.order() == gp_order:
                    gp_is_cyc = True
                    break
                    
        # Check if G' is contained in N
        gp_in_N = True
        for x in G_prime.generators:
            if x not in N:
                gp_in_N = False
                break
                
        if not gp_is_cyc or not gp_in_N:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal cyclic subgroup of G",
    "H_2: The quotient group G/N is a cyclic group",
    "¬Q: The derived subgroup G' is not cyclic or not contained in N"
]

N_HYP = 2
NEG_Q_INDEX = 2