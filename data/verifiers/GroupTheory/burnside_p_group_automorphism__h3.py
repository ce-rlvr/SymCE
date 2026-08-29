import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_order(G):
    order = G.order
    if callable(order):
        return order()
    return order

def get_elements(G):
    elems = G.elements
    if callable(elems):
        return elems()
    return elems

def apply_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha[x]
    else:
        return alpha(x)

def get_p(G):
    try:
        order = get_order(G)
        if order == 1:
            return None
        factors = sympy.ntheory.factorint(int(order))
        if len(factors) == 1:
            return list(factors.keys())[0]
        return None
    except Exception:
        return None

def frattini_subgroup(G, p):
    derived = G.derived_subgroup
    if callable(derived):
        derived = derived()
    gens = list(derived.generators)
    p_int = int(p)
    for g in get_elements(G):
        gens.append(g**p_int)
    gens = [g for g in gens if not g.is_Identity]
    if not gens:
        return PermutationGroup(G.identity)
    return PermutationGroup(*gens)

def _lcm(a, b):
    a, b = int(a), int(b)
    return abs(a * b) // math.gcd(a, b)

def get_alpha_order(G, alpha):
    elements = list(get_elements(G))
    elements_set = set(elements)
    mapped = []
    for x in elements:
        ax = apply_alpha(alpha, x)
        if ax not in elements_set:
            return None
        mapped.append(ax)
    if len(set(mapped)) != len(elements):
        return None
    
    visited = set()
    lcm = 1
    for x in elements:
        if x not in visited:
            curr = x
            length = 0
            while True:
                visited.add(curr)
                curr = apply_alpha(alpha, curr)
                length += 1
                if curr == x:
                    break
                if curr in visited:
                    return None
            lcm = _lcm(lcm, length)
    return lcm

def conditions(witness):
    try:
        if len(witness) == 2:
            G, alpha = witness
            Phi_given = None
        elif len(witness) == 3:
            G, Phi_given, alpha = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite p-group for some prime p
    try:
        p = get_p(G)
        h1 = (p is not None)
    except Exception:
        h1 = False
        p = None

    # H_2: Phi(G) is the Frattini subgroup of G
    try:
        if p is not None:
            Phi = frattini_subgroup(G, p)
            if Phi_given is not None:
                h2 = (set(get_elements(Phi_given)) == set(get_elements(Phi)))
            else:
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: The order of alpha is coprime to p
    try:
        if p is not None:
            order_alpha = get_alpha_order(G, alpha)
            h3 = (order_alpha is not None) and (math.gcd(int(order_alpha), int(p)) == 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: alpha(x * Phi(G)) = x * Phi(G) for all x in G
    try:
        if p is not None and h2:
            phi_elements = set(get_elements(Phi))
            h4 = True
            for x in get_elements(G):
                ax = apply_alpha(alpha, x)
                if (x**-1 * ax) not in phi_elements:
                    h4 = False
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: alpha is not the identity automorphism of G
    try:
        neg_q = False
        for x in get_elements(G):
            if apply_alpha(alpha, x) != x:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group for some prime p",
    "H_2: Phi(G) is the Frattini subgroup of G",
    "H_3: The order of alpha is coprime to p",
    "H_4: alpha(x * Phi(G)) = x * Phi(G) for all x in G",
    "¬Q: alpha is not the identity automorphism of G"
]

N_HYP = 4
NEG_Q_INDEX = 4