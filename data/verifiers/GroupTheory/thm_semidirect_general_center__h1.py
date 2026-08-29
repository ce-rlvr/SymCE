import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def is_subgroup(sub, supergroup):
    return all(g in supergroup for g in sub.generators)

def is_normal(sub, supergroup):
    if not is_subgroup(sub, supergroup):
        return False
    for g in supergroup.generators:
        for n in sub.generators:
            if (g * n * ~g) not in sub:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G, N, H are PermutationGroups and N, H are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(H, PermutationGroup) and
              is_subgroup(N, G) and is_subgroup(H, G))
    except Exception:
        h1 = False

    # H_2: G is the internal semidirect product of N and H
    try:
        normal_N = is_normal(N, G)
        n_elements = set(N.elements)
        h_elements = set(H.elements)
        intersect_trivial = len(n_elements.intersection(h_elements)) == 1
        order_correct = G.order() == N.order() * H.order()
        h2 = bool(normal_N and intersect_trivial and order_correct)
    except Exception:
        h2 = False

    # neg_Q: Z(G) is not isomorphic to (Z(N) \cap C_N(H)) \times (Z(H) \cap \ker(\phi))
    try:
        def get_center(group):
            gens = group.generators
            c_elems = []
            for g in group.elements:
                if all(g * x == x * g for x in gens):
                    c_elems.append(g)
            return PermutationGroup(c_elems) if c_elems else PermutationGroup([group.identity])
            
        Z_G = get_center(G)
        Z_N = get_center(N)
        Z_H = get_center(H)
        
        # C_N(H)
        gens_H = H.generators
        cn_h_elems = []
        for n in N.elements:
            if all(h * n * ~h == n for h in gens_H):
                cn_h_elems.append(n)
                
        # Z(N) \cap C_N(H)
        zn_elems = set(Z_N.elements)
        part1_elems = [n for n in cn_h_elems if n in zn_elems]
        part1_group = PermutationGroup(part1_elems) if part1_elems else PermutationGroup([G.identity])
        
        # \ker(\phi) = H \cap C_G(N)
        gens_N = N.generators
        ker_elems = []
        for h in H.elements:
            if all(h * n * ~h == n for n in gens_N):
                ker_elems.append(h)
                
        # Z(H) \cap \ker(\phi)
        zh_elems = set(Z_H.elements)
        part2_elems = [h for h in ker_elems if h in zh_elems]
        part2_group = PermutationGroup(part2_elems) if part2_elems else PermutationGroup([G.identity])
        
        # Direct product of part1_group and part2_group
        deg1 = max(part1_group.degree, 1)
        deg2 = max(part2_group.degree, 1)
        dp_gens = []
        
        def apply_perm(g, i):
            if i < g.size:
                return g.array_form[i]
            return i
            
        for g in part1_group.generators:
            if g.is_Identity: continue
            arr = [apply_perm(g, i) for i in range(deg1)] + [deg1 + i for i in range(deg2)]
            dp_gens.append(Permutation(arr))
            
        for g in part2_group.generators:
            if g.is_Identity: continue
            arr = [i for i in range(deg1)] + [deg1 + apply_perm(g, i) for i in range(deg2)]
            dp_gens.append(Permutation(arr))
            
        if not dp_gens:
            DP = PermutationGroup([Permutation(deg1 + deg2 - 1)])
        else:
            DP = PermutationGroup(dp_gens)
            
        # For finite abelian groups, the multiset of element orders uniquely determines the isomorphism class
        orders_G = sorted([g.order() for g in Z_G.elements])
        orders_DP = sorted([g.order() for g in DP.elements])
        
        neg_q = (orders_G != orders_DP)
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, H are PermutationGroups and N, H are subgroups of G",
    "H_2: G is the internal semidirect product of N and H",
    "¬Q: Z(G) is not isomorphic to (Z(N) ∩ C_N(H)) × (Z(H) ∩ ker(φ))"
]

N_HYP = 2
NEG_Q_INDEX = 2