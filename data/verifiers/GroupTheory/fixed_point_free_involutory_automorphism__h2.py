import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _eval_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha[x]
    elif callable(alpha):
        return alpha(x)
    else:
        for k, v in alpha:
            if k == x:
                return v
        raise ValueError("x not found in alpha")

def conditions(witness) -> list[bool]:
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'identity') and hasattr(G, 'is_abelian')
        if h1:
            elements = list(G.elements)
            h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H_2: alpha(alpha(x)) = x for all x in G
    try:
        elements = list(G.elements)
        h2 = True
        for x in elements:
            ax = _eval_alpha(alpha, x)
            if ax not in elements:
                h2 = False
                break
            aax = _eval_alpha(alpha, ax)
            if aax != x:
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: For all x in G, alpha(x) = x implies x = e
    try:
        elements = list(G.elements)
        e = G.identity
        h3 = True
        for x in elements:
            ax = _eval_alpha(alpha, x)
            if ax == x and x != e:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: G is not an abelian group or alpha(x) != x^-1 for some x in G
    try:
        elements = list(G.elements)
        is_abelian = bool(G.is_abelian)
        alpha_is_inv = True
        for x in elements:
            ax = _eval_alpha(alpha, x)
            if ax != x**-1:
                alpha_is_inv = False
                break
        neg_q = not (is_abelian and alpha_is_inv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha(alpha(x)) = x for all x in G",
    "H_3: For all x in G, alpha(x) = x implies x = e",
    "¬Q: G is not an abelian group or alpha(x) != x^-1 for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3