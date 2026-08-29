import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    try:
        return list(G.elements)
    except Exception:
        return list(G.generate())

def is_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    H_elems = get_elements(H)
    G_elems = get_elements(G)
    for h in H_elems:
        if h not in G_elems:
            return False
    return True

def is_normal_subgroup(H, G):
    if not is_subgroup(H, G):
        return False
    H_elems = get_elements(H)
    G_elems = get_elements(G)
    for g in G_elems:
        for h in H_elems:
            if g * h * ~g not in H_elems:
                return False
    return True

def intersect_groups(G1, G2):
    if not isinstance(G1, PermutationGroup) or not isinstance(G2, PermutationGroup):
        return None
    common = list(set(get_elements(G1)).intersection(set(get_elements(G2))))
    return PermutationGroup(common)

def get_product_group(H, K):
    if H is None or K is None:
        return None
    elems = set()
    H_elems = get_elements(H)
    K_elems = get_elements(K)
    for h in H_elems:
        for k in K_elems:
            elems.add(h * k)
    
    for x in elems:
        for y in elems:
            if x * y not in elems:
                return None
    return PermutationGroup(list(elems))

def quotient_group(N, D):
    if N is None or D is None:
        return None
    if not is_normal_subgroup(D, N):
        return None
        
    N_elems = get_elements(N)
    D_elems = get_elements(D)
    
    coset_reps = []
    for x in N_elems:
        found = False
        for rep in coset_reps:
            if (x * ~rep) in D_elems:
                found = True
                break
        if not found:
            coset_reps.append(x)
            
    perms = []
    for g in coset_reps:
        p = []
        for x in coset_reps:
            prod = g * x
            for i, rep in enumerate(coset_reps):
                if (prod * ~rep) in D_elems:
                    p.append(i)
                    break
        perms.append(Permutation(p))
        
    return PermutationGroup(perms)

def are_isomorphic(G1, G2):
    G1_elems = get_elements(G1)
    G2_elems = get_elements(G2)
    
    if len(G1_elems) != len(G2_elems):
        return False
    if hasattr(G1, 'is_isomorphic'):
        try:
            return G1.is_isomorphic(G2)
        except Exception:
            pass
            
    orders1 = sorted([g.order() for g in G1_elems])
    orders2 = sorted([g.order() for g in G2_elems])
    if orders1 != orders2:
        return False
        
    n = len(G1_elems)
    
    id1 = next(g for g in G1_elems if g.order() == 1)
    id2 = next(g for g in G2_elems if g.order() == 1)
    
    gens1 = G1.generators
    for gen_map in itertools.permutations(G2_elems, len(gens1)):
        if any(g.order() != m.order() for g, m in zip(gens1, gen_map)):
            continue
            
        mapping = {id1: id2}
        for g, m in zip(gens1, gen_map):
            mapping[g] = m
            
        valid = True
        queue = list(gens1)
        while queue:
            curr = queue.pop(0)
            for g in gens1:
                prod = curr * g
                prod_map = mapping[curr] * mapping[g]
                if prod in mapping:
                    if mapping[prod] != prod_map:
                        valid = False
                        break
                else:
                    mapping[prod] = prod_map
                    queue.append(prod)
            if not valid:
                break
        if valid and len(mapping) == n and len(set(mapping.values())) == n:
            return True
    return False

def conditions(witness):
    try:
        G, A, A_star, B, B_star = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G
    try:
        h2 = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h2 = False

    # H3: A^* is a normal subgroup of A
    try:
        h3 = is_normal_subgroup(A_star, A)
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails
    try:
        if not isinstance(B_star, PermutationGroup):
            neg_q = True
        else:
            A_cap_B = intersect_groups(A, B)
            A_cap_B_star = intersect_groups(A, B_star)
            A_star_cap_B = intersect_groups(A_star, B)
            
            num1 = get_product_group(A_cap_B, A_star)
            den1 = get_product_group(A_cap_B_star, A_star)
            
            num2 = get_product_group(A_cap_B, B_star)
            den2 = get_product_group(A_star_cap_B, B_star)
            
            Q1 = quotient_group(num1, den1)
            Q2 = quotient_group(num2, den2)
            
            if Q1 is None or Q2 is None:
                neg_q = True
            else:
                neg_q = not are_isomorphic(Q1, Q2)
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A and B are subgroups of G",
    "H_3: A^* is a normal subgroup of A",
    "¬Q: (A \\cap B)A^* / (A \\cap B^*)A^* \\not\\cong (A \\cap B)B^* / (A^* \\cap B)B^*"
]

N_HYP = 3
NEG_Q_INDEX = 3