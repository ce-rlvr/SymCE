import math
import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, N, F = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N, G, and F are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(F, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: 1 -> N -> G -> F -> 1 is a short exact sequence
    try:
        if not h1:
            h2 = False
        else:
            is_sub = N.is_subgroup(G)
            is_norm = N.is_normal(G)
            order_ok = int(G.order()) == int(N.order()) * int(F.order())
            
            def order_profile(grp):
                profile = {}
                for g in grp.generate():
                    o = g.order()
                    profile[o] = profile.get(o, 0) + 1
                return profile

            def quotient_order_profile(G, N):
                N_elements = list(N.generate())
                coset_reps = []
                for g in G.generate():
                    is_new = True
                    for c_rep in coset_reps:
                        if ((~c_rep) * g) in N_elements:
                            is_new = False
                            break
                    if is_new:
                        coset_reps.append(g)
                        
                profile = {}
                for c_rep in coset_reps:
                    for k in range(1, int(G.order()) + 1):
                        if (c_rep**k) in N_elements:
                            profile[k] = profile.get(k, 0) + 1
                            break
                return profile

            def quotient_is_abelian(G, N):
                N_elements = set(N.generate())
                for g1 in G.generators:
                    for g2 in G.generators:
                        comm = (~g1) * (~g2) * g1 * g2
                        if comm not in N_elements:
                            return False
                return True

            if is_sub and is_norm and order_ok:
                iso_ok = (order_profile(F) == quotient_order_profile(G, N)) and (bool(F.is_abelian) == quotient_is_abelian(G, N))
                h2 = iso_ok
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The sequence does NOT split, or G is NOT isomorphic to a semidirect product of N and F
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            target_order = int(G.order()) // int(N.order())
            N_elements = set(N.generate())
            G_elements = list(G.generate())
            
            if target_order == 1:
                splits = True
            else:
                valid_elements = [g for g in G_elements if target_order % g.order() == 0]
                
                def get_subgroup(gens):
                    elements = set()
                    frontier = list(gens)
                    while frontier:
                        curr = frontier.pop()
                        if curr not in elements:
                            # If it's not the identity and it's in N, intersection is non-trivial
                            if curr != curr**0 and curr in N_elements:
                                return None 
                            elements.add(curr)
                            if len(elements) > target_order:
                                return None
                            for g in list(elements):
                                frontier.append(curr * g)
                                frontier.append(g * curr)
                    return elements

                max_gens = int(math.log2(target_order)) + 1
                splits = False
                for r in range(1, max_gens + 1):
                    for gens in itertools.combinations(valid_elements, r):
                        sg = get_subgroup(gens)
                        if sg is not None and len(sg) == target_order:
                            splits = True
                            break
                    if splits:
                        break
            
            neg_q = not splits
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N, G, and F are groups",
    "H_2: 1 -> N -> G -> F -> 1 is a short exact sequence",
    "¬Q: The sequence does not split, or G is not isomorphic to a semidirect product of N and F"
]

N_HYP = 2
NEG_Q_INDEX = 2