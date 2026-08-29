import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G):
    return hasattr(G, 'elements') and hasattr(G, 'identity')

def is_map(K, G, f):
    try:
        K_elements = list(K.elements)
        G_elements = list(G.elements)
        for x in K_elements:
            fx = f(x) if callable(f) else f[x]
            if fx not in G_elements:
                return False
        return True
    except Exception:
        return False

def is_homomorphism(K, G, f):
    try:
        if not is_map(K, G, f):
            return False
        K_elements = list(K.elements)
        for x in K_elements:
            for y in K_elements:
                fx = f(x) if callable(f) else f[x]
                fy = f(y) if callable(f) else f[y]
                fxy = f(x * y) if callable(f) else f[x * y]
                if fxy != fx * fy:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G1, G2, K, f1, f2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G_1, G_2, and K are groups
    try:
        h1 = is_group(G1) and is_group(G2) and is_group(K)
    except Exception:
        h1 = False

    # H_2: f_1: K -> G_1 is a group homomorphism
    try:
        h2 = is_homomorphism(K, G1, f1)
    except Exception:
        h2 = False

    # H_3: f_2: K -> G_2 is a well-defined map
    try:
        h3 = is_map(K, G2, f2)
    except Exception:
        h3 = False

    # ¬Q: There does not exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2
    # Since f(x) = (f_1(x), f_2(x)) is the only possible map satisfying the projection conditions,
    # it is a valid group homomorphism if and only if both f_1 and f_2 are group homomorphisms.
    # Given that f_1 is a homomorphism (H_2), f is a homomorphism iff f_2 is a homomorphism.
    # Therefore, the conclusion fails (¬Q is True) iff f_2 is NOT a group homomorphism.
    try:
        if not h3:
            neg_q = False
        else:
            neg_q = not is_homomorphism(K, G2, f2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G_1, G_2, and K are groups",
    "H_2: f_1: K -> G_1 is a group homomorphism",
    "H_3: f_2: K -> G_2 is a well-defined map (and pi_1, pi_2 are canonical projections)",
    "¬Q: There does not exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2"
]

N_HYP = 3
NEG_Q_INDEX = 3