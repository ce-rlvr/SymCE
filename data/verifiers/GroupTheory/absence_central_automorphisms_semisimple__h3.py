import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['alpha']
    return witness[0], witness[1]

def apply_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    return alpha(g)

def is_automorphism(G, alpha):
    elements = list(G.elements)
    mapped = []
    for g in elements:
        ag = apply_alpha(alpha, g)
        if ag not in elements:
            return False
        mapped.append(ag)
    if len(set(mapped)) != len(elements):
        return False
    for x in elements:
        for y in elements:
            if apply_alpha(alpha, x * y) != apply_alpha(alpha, x) * apply_alpha(alpha, y):
                return False
    return True

def is_semisimple(G):
    try:
        elements = list(G.elements)
        gens = G.generators
        
        # Center of G
        Z_elems = [g for g in elements if all(g * h == h * g for h in gens)]
        
        # Check if the center is elementary abelian (square-free exponent)
        exp = 1
        for g in Z_elems:
            exp = _lcm(exp, g.order())
        for p in sympy.primefactors(exp):
            if exp % (p * p) == 0:
                return False
                
        # Derived subgroup D of G
        comms = []
        for x in elements:
            for y in elements:
                comms.append(x**-1 * y**-1 * x * y)
        D = PermutationGroup(comms)
        
        # Derived subgroup of D
        D_elements = list(D.elements)
        D_comms = []
        for x in D_elements:
            for y in D_elements:
                D_comms.append(x**-1 * y**-1 * x * y)
        D_derived = PermutationGroup(D_comms)
        
        # D must be perfect
        if D_derived.order() != D.order():
            return False
            
        # G must be the direct product of D and Z
        if G.order() != D.order() * len(Z_elems):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, alpha = parse_witness(witness)
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group and alpha is an automorphism
    try:
        h1 = False
        if hasattr(G, 'elements') and hasattr(G, 'order'):
            if G.order() > 0:
                h1 = is_automorphism(G, alpha)
    except Exception:
        h1 = False

    # H2: G is a semisimple group
    try:
        h2 = is_semisimple(G)
    except Exception:
        h2 = False

    # H3: For all elements g in G, g^{-1}*alpha(g) belongs to the center of G
    try:
        h3 = True
        elements = list(G.elements)
        gens = G.generators
        Z_elems = [g for g in elements if all(g * h == h * g for h in gens)]
        for g in elements:
            ag = apply_alpha(alpha, g)
            val = g**-1 * ag
            if val not in Z_elems:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: The automorphism alpha is not the identity automorphism on G
    try:
        neg_q = False
        elements = list(G.elements)
        for g in elements:
            if apply_alpha(alpha, g) != g:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and alpha is an automorphism",
    "H_2: G is a semisimple group",
    "H_3: For all elements g in G, g^{-1}*alpha(g) belongs to the center of G",
    "¬Q: The automorphism alpha is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3