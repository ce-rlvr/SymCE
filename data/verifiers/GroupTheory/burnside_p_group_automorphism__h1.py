import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def get_all_subgroups(G):
    elements = list(G.elements)
    id_elem = elements[0]**0
    trivial_elems = frozenset([id_elem])
    seen = {trivial_elems}
    queue = [(trivial_elems, [])]
    
    while queue:
        H_elems, H_gens = queue.pop(0)
        for x in elements:
            if x not in H_elems:
                new_gens = H_gens + [x]
                K = PermutationGroup(new_gens)
                K_elems = frozenset(K.elements)
                if K_elems not in seen:
                    seen.add(K_elems)
                    queue.append((K_elems, new_gens))
    return seen

def get_maximal_subgroups(G):
    G_elems = frozenset(G.elements)
    subgroups = get_all_subgroups(G)
    proper_subgroups = [H for H in subgroups if H != G_elems]
    maximal = []
    for H in proper_subgroups:
        is_max = True
        for K in proper_subgroups:
            if H != K and H.issubset(K):
                is_max = False
                break
        if is_max:
            maximal.append(H)
    return maximal

def frattini_subgroup_elements(G):
    max_subs = get_maximal_subgroups(G)
    if not max_subs:
        return frozenset(G.elements)
    phi = set(max_subs[0])
    for H in max_subs[1:]:
        phi = phi.intersection(H)
    return frozenset(phi)

def is_automorphism(G, alpha_dict):
    elements = list(G.elements)
    if len(set(alpha_dict.values())) != len(elements):
        return False
    for x in elements:
        if alpha_dict[x] not in elements:
            return False
    for x in elements:
        for y in elements:
            if alpha_dict[x * y] != alpha_dict[x] * alpha_dict[y]:
                return False
    return True

def get_alpha_order(G_elems, alpha_dict):
    visited = set()
    order = 1
    for x in G_elems:
        if x not in visited:
            curr = x
            length = 0
            while True:
                visited.add(curr)
                curr = alpha_dict[curr]
                length += 1
                if curr == x:
                    break
                if length > len(G_elems):
                    raise ValueError("Not a bijection")
            order = math.lcm(order, length)
    return order

CONDITION_LABELS = [
    "H_1: Phi(G) is the Frattini subgroup of G",
    "H_2: alpha is an automorphism of G",
    "H_3: The order of alpha is coprime to p",
    "H_4: alpha(x*Phi(G)) = x*Phi(G) for all x in G",
    "¬Q: alpha is not the identity automorphism of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) == 3:
            G, p, alpha_obj = witness
            Phi_G_elems = None
        elif len(witness) == 4:
            G, p, alpha_obj, Phi_G_elems = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        if callable(alpha_obj):
            alpha_dict = {x: alpha_obj(x) for x in G.elements}
        else:
            alpha_dict = alpha_obj
    except Exception:
        return [False] * 5

    # H1: Phi(G) is the Frattini subgroup of G
    try:
        actual_phi = frattini_subgroup_elements(G)
        if Phi_G_elems is not None:
            h1_ok = (set(Phi_G_elems) == actual_phi)
            phi_to_use = set(Phi_G_elems)
        else:
            h1_ok = True
            phi_to_use = actual_phi
    except Exception:
        h1_ok = False
        phi_to_use = set()

    # H2: alpha is an automorphism of G
    try:
        h2_ok = is_automorphism(G, alpha_dict)
    except Exception:
        h2_ok = False

    # H3: The order of alpha is coprime to p
    try:
        if sympy.isprime(p):
            order = get_alpha_order(list(G.elements), alpha_dict)
            h3_ok = (math.gcd(order, p) == 1)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # H4: alpha(x*Phi(G)) = x*Phi(G) for all x in G
    try:
        h4_ok = True
        for x in G.elements:
            if (x**-1 * alpha_dict[x]) not in phi_to_use:
                h4_ok = False
                break
    except Exception:
        h4_ok = False

    # neg_Q: alpha is not the identity automorphism of G
    try:
        neg_q_ok = False
        for x in G.elements:
            if alpha_dict[x] != x:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]