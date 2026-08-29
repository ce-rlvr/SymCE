import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

# Top-level setup for named groups
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

def custom_direct_product(G1, G2, d1=None, d2=None):
    """Constructs the external direct product of two permutation groups."""
    if d1 is None:
        d1 = G1.degree
    else:
        d1 = max(d1, G1.degree)
        
    if d2 is None:
        d2 = G2.degree
    else:
        d2 = max(d2, G2.degree)
        
    gens = []
    for g in G1.generators:
        p = list(g.array_form)
        if len(p) < d1:
            p += list(range(len(p), d1))
        p += list(range(d1, d1 + d2))
        gens.append(Permutation(p))
        
    for h in G2.generators:
        p = list(range(d1))
        h_arr = list(h.array_form)
        if len(h_arr) < d2:
            h_arr += list(range(len(h_arr), d2))
        p += [x + d1 for x in h_arr]
        gens.append(Permutation(p))
        
    if not gens:
        if d1 + d2 > 0:
            return PermutationGroup([Permutation(d1 + d2 - 1)])
        else:
            return PermutationGroup([Permutation()])
    return PermutationGroup(gens)

def get_quotient_group(G, N):
    """Constructs a permutation group isomorphic to the quotient group G/N."""
    N_elems = set(N.generate())
    if not N_elems:
        N_elems = {Permutation()}
        
    id_perm = list(N_elems)[0] ** 0
    
    coset_reps = [id_perm]
    elem_to_coset = {}
    for n in N_elems:
        elem_to_coset[n] = 0
        
    queue = [id_perm]
    head = 0
    while head < len(queue):
        curr = queue[head]
        head += 1
        
        for gen in G.generators:
            nxt = curr * gen
            if nxt not in elem_to_coset:
                new_coset_idx = len(coset_reps)
                coset_reps.append(nxt)
                queue.append(nxt)
                for n in N_elems:
                    nx = n * nxt
                    elem_to_coset[nx] = new_coset_idx
                    
    n_cosets = len(coset_reps)
    quotient_gens = []
    for gen in G.generators:
        p = []
        for j in range(n_cosets):
            prod = gen * coset_reps[j]
            p.append(elem_to_coset.get(prod, 0))
        quotient_gens.append(Permutation(p))
        
    if not quotient_gens:
        if n_cosets > 0:
            return PermutationGroup([Permutation(n_cosets - 1)])
        else:
            return PermutationGroup([Permutation()])
    return PermutationGroup(quotient_gens)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Witness should be a tuple of 4 PermutationGroups: (G1, G2, N1, N2)
    """
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(N1.is_subgroup(G1) and G1.is_normal(N1))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(N2.is_subgroup(G2) and G2.is_normal(N2))
    except Exception:
        h2 = False
        
    try:
        d1 = max(G1.degree, N1.degree)
        d2 = max(G2.degree, N2.degree)
        
        G1xG2 = custom_direct_product(G1, G2, d1, d2)
        N1xN2 = custom_direct_product(N1, N2, d1, d2)
        
        is_normal_prod = bool(N1xN2.is_subgroup(G1xG2) and G1xG2.is_normal(N1xN2))
        
        if not is_normal_prod:
            neg_q = True
        else:
            Q_prod = get_quotient_group(G1xG2, N1xN2)
            Q1 = get_quotient_group(G1, N1)
            Q2 = get_quotient_group(G2, N2)
            Q1xQ2 = custom_direct_product(Q1, Q2)
            
            is_iso = bool(Q_prod.is_isomorphic(Q1xQ2))
            neg_q = not is_iso
            
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N_1 is a normal subgroup of G_1",
    "H_2: N_2 is a normal subgroup of G_2",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or (G_1 x G_2)/(N_1 x N_2) is not isomorphic to (G_1/N_1) x (G_2/N_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2