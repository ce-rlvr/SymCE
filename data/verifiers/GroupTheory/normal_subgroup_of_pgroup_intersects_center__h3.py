import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: N is not the trivial subgroup",
    "¬Q: The intersection of N and the center Z(G) is the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        p, G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        p_int = int(p)
        h1 = bool(isprime(p_int))
    except Exception:
        h1 = False

    # H_2: G is a finite p-group
    try:
        p_int = int(p)
        order = G.order()
        if order < 1:
            h2 = False
        else:
            temp = int(order)
            h2 = True
            if temp > 1:
                while temp > 1:
                    if temp % p_int != 0:
                        h2 = False
                        break
                    temp = temp // p_int
    except Exception:
        h2 = False

    # H_3: N is not the trivial subgroup (and is a valid subgroup of G)
    try:
        n_elems = set(N.generate()) if hasattr(N, 'generate') else set(N.elements)
        g_elems = set(G.generate()) if hasattr(G, 'generate') else set(G.elements)
        is_sub = n_elems.issubset(g_elems)
        h3 = bool(is_sub and len(n_elems) > 1)
    except Exception:
        h3 = False

    # ¬Q: The intersection of N and the center Z(G) is the trivial subgroup
    try:
        n_elems = set(N.generate()) if hasattr(N, 'generate') else set(N.elements)
        g_elems = set(G.generate()) if hasattr(G, 'generate') else set(G.elements)
        
        if hasattr(G, 'center'):
            Z = G.center()
            z_elems = set(Z.generate()) if hasattr(Z, 'generate') else set(Z.elements)
        else:
            z_elems = {x for x in g_elems if all(x * y == y * x for y in g_elems)}
            
        int_elements = n_elems.intersection(z_elems)
        neg_q = bool(len(int_elements) == 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]