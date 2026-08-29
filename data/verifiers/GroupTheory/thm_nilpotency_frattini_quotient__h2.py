import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The quotient group G/Phi(G) is nilpotent",
    "¬Q: G is not nilpotent"
]
N_HYP = 2
NEG_Q_INDEX = 2

def is_finite_group(G):
    if isinstance(G, PermutationGroup):
        return True
    if hasattr(G, 'is_finite'):
        fin = G.is_finite
        if callable(fin):
            return bool(fin())
        return bool(fin)
    if hasattr(G, 'order'):
        try:
            ord_val = G.order
            if callable(ord_val):
                ord_val = ord_val()
            return ord_val < float('inf')
        except Exception:
            pass
    return False

def get_elements(G):
    if hasattr(G, 'elements'):
        elms = G.elements
        if callable(elms):
            return list(elms())
        return list(elms)
    elif hasattr(G, 'generate_dimino'):
        gen = G.generate_dimino
        if callable(gen):
            return list(gen())
        return list(gen)
    else:
        raise ValueError("Cannot get elements")

def frattini_subgroup(G):
    elements = get_elements(G)
    if not elements:
        return G
    identity = elements[0]**0
    
    def get_closure(gens):
        c = set(gens)
        c.add(identity)
        frontier = list(c)
        while frontier:
            new_frontier = []
            for g in frontier:
                for h in gens:
                    gh = g * h
                    if gh not in c:
                        c.add(gh)
                        new_frontier.append(gh)
            frontier = new_frontier
        return frozenset(c)

    subgroups = {}
    
    for g in elements:
        H = get_closure([g])
        if H not in subgroups:
            subgroups[H] = [g]
            
    current_level = list(subgroups.keys())
    while current_level:
        next_level = {}
        for H in current_level:
            if len(H) == len(elements):
                continue
            gens_H = subgroups[H]
            for g in elements:
                if g not in H:
                    new_gens = gens_H + [g]
                    new_H = get_closure(new_gens)
                    if new_H not in subgroups and new_H not in next_level:
                        next_level[new_H] = new_gens
        subgroups.update(next_level)
        current_level = list(next_level.keys())
        
    G_set = frozenset(elements)
    proper_subgroups = [H for H in subgroups.keys() if H != G_set]
    maximal_subgroups = []
    for H in proper_subgroups:
        is_maximal = True
        for K in proper_subgroups:
            if H != K and H.issubset(K):
                is_maximal = False
                break
        if is_maximal:
            maximal_subgroups.append(H)
            
    if not maximal_subgroups:
        return PermutationGroup([identity])
        
    phi_elements = set.intersection(*maximal_subgroups)
    return PermutationGroup(list(phi_elements))

def quotient_is_nilpotent(G, N):
    lcs = G.lower_central_series
    if callable(lcs):
        lcs = lcs()
    limit_group = lcs[-1]
    N_elements = set(get_elements(N))
    for g in limit_group.generators:
        if g not in N_elements:
            return False
    return True

def check_nilpotent(G):
    if hasattr(G, 'is_nilpotent'):
        nilp = G.is_nilpotent
        if callable(nilp):
            return bool(nilp())
        return bool(nilp)
    if hasattr(G, 'lower_central_series'):
        lcs = G.lower_central_series
        if callable(lcs):
            lcs = lcs()
        ord_val = lcs[-1].order
        if callable(ord_val):
            ord_val = ord_val()
        return ord_val == 1
    raise ValueError("Not a group")

def conditions(witness):
    try:
        h1 = is_finite_group(witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            Phi = frattini_subgroup(witness)
            h2 = quotient_is_nilpotent(witness, Phi)
    except Exception:
        h2 = False

    try:
        neg_q = not check_nilpotent(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]