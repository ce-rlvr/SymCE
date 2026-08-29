import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def evaluate_f(f, x):
    if isinstance(f, dict):
        return f[x]
    else:
        return f(x)

def is_homomorphism(G_elements, H_elements, f):
    for g in G_elements:
        try:
            fg = evaluate_f(f, g)
        except Exception:
            return False
        if fg not in H_elements:
            return False
    for g1 in G_elements:
        for g2 in G_elements:
            if evaluate_f(f, g1 * g2) != evaluate_f(f, g1) * evaluate_f(f, g2):
                return False
    return True

def is_surjective(G_elements, H_elements, f):
    image = {evaluate_f(f, g) for g in G_elements}
    return image == set(H_elements)

def normalizer(group_elements, subset):
    subset_set = set(subset)
    norm = set()
    for g in group_elements:
        try:
            g_inv = g**-1
        except Exception:
            g_inv = ~g
        conj = {g * s * g_inv for s in subset_set}
        if conj == subset_set:
            norm.add(g)
    return norm

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        S = witness['S']
    except Exception:
        return [False, False, False]
    
    try:
        G_elements = get_elements(G)
        H_elements = get_elements(H)
    except Exception:
        return [False, False, False]

    # H_1: f: G \to H is a surjective group homomorphism
    try:
        h1_ok = is_homomorphism(G_elements, H_elements, f) and is_surjective(G_elements, H_elements, f)
    except Exception:
        h1_ok = False

    # H_2: S is a subset of G
    try:
        S_set = set(S)
        G_set = set(G_elements)
        h2_ok = S_set.issubset(G_set)
    except Exception:
        h2_ok = False

    # neg_Q: f(N_G(S)) \subseteq N_H(f(S)) FAILS
    try:
        N_G_S = normalizer(G_elements, S_set)
        f_S = {evaluate_f(f, s) for s in S_set}
        N_H_fS = normalizer(H_elements, f_S)
        
        f_N_G_S = {evaluate_f(f, g) for g in N_G_S}
        
        neg_q_ok = not f_N_G_S.issubset(N_H_fS)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "H_2: S is a subset of G",
    "¬Q: f(N_G(S)) is not a subset of N_H(f(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2