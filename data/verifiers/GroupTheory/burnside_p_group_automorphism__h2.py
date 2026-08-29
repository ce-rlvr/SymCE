import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory
import math
import itertools
import functools

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

def apply_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    return alpha(g)

def get_lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def frattini_subgroup(G, p):
    elements = list(G.generate())
    generators = [g**p for g in elements]
    for g in elements:
        for h in elements:
            generators.append(g**-1 * h**-1 * g * h)
    
    closure = set(generators)
    closure.add(G.identity)
    added = True
    while added:
        added = False
        new_elements = set()
        for a in closure:
            for b in generators:
                c = a * b
                if c not in closure:
                    new_elements.add(c)
        if new_elements:
            closure.update(new_elements)
            added = True
    return closure

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, alpha = witness
        else:
            G = getattr(witness, 'G', None)
            alpha = getattr(witness, 'alpha', None)
            if G is None or alpha is None:
                return [False] * 5
    except Exception:
        return [False] * 5
    
    # H1: G is a finite p-group
    try:
        elements = list(G.generate())
        n = len(elements)
        if n == 1:
            p = 2
            h1 = True
        else:
            factors = sympy.ntheory.factorint(n)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                h1 = True
            else:
                p = None
                h1 = False
    except Exception:
        h1 = False
        p = None

    # H2: alpha is an automorphism of G
    try:
        h2 = True
        mapped = set()
        for g in elements:
            ag = apply_alpha(alpha, g)
            if ag not in elements:
                h2 = False
                break
            mapped.add(ag)
        if h2 and len(mapped) != len(elements):
            h2 = False
        if h2:
            for g in elements:
                for h in elements:
                    if apply_alpha(alpha, g * h) != apply_alpha(alpha, g) * apply_alpha(alpha, h):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: order of alpha is coprime to p
    try:
        if h1 and h2:
            visited = set()
            order = 1
            for g in elements:
                if g not in visited:
                    cycle_len = 0
                    curr = g
                    while True:
                        visited.add(curr)
                        curr = apply_alpha(alpha, curr)
                        cycle_len += 1
                        if curr == g:
                            break
                    order = get_lcm(order, cycle_len)
            h3 = (math.gcd(order, p) == 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: alpha(x Phi(G)) = x Phi(G)
    try:
        if h1 and h2:
            phi = frattini_subgroup(G, p)
            h4 = True
            for x in elements:
                ax = apply_alpha(alpha, x)
                if x**-1 * ax not in phi:
                    h4 = False
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: alpha is NOT the identity
    try:
        if h2:
            neg_q = False
            for x in elements:
                if apply_alpha(alpha, x) != x:
                    neg_q = True
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group for some prime p",
    "H_2: alpha is an automorphism of G",
    "H_3: The order of alpha is coprime to p",
    "H_4: alpha(x*Phi(G)) = x*Phi(G) for all x in G",
    "¬Q: alpha is not the identity automorphism of G"
]

N_HYP = 4
NEG_Q_INDEX = 4