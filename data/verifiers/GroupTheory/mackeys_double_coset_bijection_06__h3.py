import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or (hasattr(G, 'elements') and hasattr(G, 'identity'))
        if h1:
            g_elems = list(G.elements)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'elements'):
            h_elems = list(H.elements)
        else:
            h_elems = list(H)
            
        h2 = True
        for h in h_elems:
            if h not in g_elems:
                h2 = False
                break
        if h2:
            if G.identity not in h_elems:
                h2 = False
            else:
                for h1_elem in h_elems:
                    if h1_elem**-1 not in h_elems:
                        h2 = False
                        break
                    for h2_elem in h_elems:
                        if h1_elem * h2_elem not in h_elems:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: G acts on the set of left cosets G/K by left multiplication
    try:
        if hasattr(K, 'elements'):
            k_elems = list(K.elements)
        else:
            k_elems = list(K)
            
        G_mod_K = set()
        for g in g_elems:
            coset = frozenset(g * k for k in k_elems)
            G_mod_K.add(coset)
            
        h3 = True
        for g in g_elems:
            for coset in G_mod_K:
                g_coset = frozenset(g * c for c in coset)
                if g_coset not in G_mod_K:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: The natural map is not a bijection
    try:
        orbits = set()
        for coset in G_mod_K:
            orbit = frozenset(frozenset(h * c for c in coset) for h in h_elems)
            orbits.add(orbit)
            
        double_cosets = set()
        for g in g_elems:
            double_coset = frozenset(h * g * k for h in h_elems for k in k_elems)
            double_cosets.add(double_coset)
            
        # The natural map is always surjective. It is a bijection iff the domain and codomain have the same size.
        neg_q = len(orbits) != len(double_cosets)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G acts on the set of left cosets G/K by left multiplication",
    "¬Q: There is no natural bijection between the orbits of H on G/K and the set of double cosets H \\ G / K"
]

N_HYP = 3
NEG_Q_INDEX = 3