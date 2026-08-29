import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
        if h1_ok:
            elements = list(G.elements)
        else:
            elements = []
    except Exception:
        h1_ok = False
        elements = []

    # H_2: alpha is an automorphism of G
    try:
        if not h1_ok:
            h2_ok = False
        else:
            if callable(alpha):
                mapping = {g: alpha(g) for g in elements}
            elif isinstance(alpha, dict):
                mapping = alpha
            else:
                mapping = {}
            
            if set(mapping.keys()) != set(elements) or set(mapping.values()) != set(elements):
                h2_ok = False
            else:
                h2_ok = True
                for g in elements:
                    for h in elements:
                        if mapping[g * h] != mapping[g] * mapping[h]:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
    except Exception:
        h2_ok = False

    # H_3: alpha(alpha(x)) = x for all x in G
    try:
        if not h1_ok or not h2_ok:
            h3_ok = False
        else:
            h3_ok = True
            for g in elements:
                if mapping[mapping[g]] != g:
                    h3_ok = False
                    break
    except Exception:
        h3_ok = False

    # neg_Q: G is not an abelian group or alpha(x) != x^-1 for some x in G
    try:
        if not h1_ok or not h2_ok:
            neg_q_ok = False
        else:
            is_abelian = bool(G.is_abelian)
            is_inversion = True
            for g in elements:
                if mapping[g] != g**-1:
                    is_inversion = False
                    break
            neg_q_ok = not (is_abelian and is_inversion)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha is an automorphism of G",
    "H_3: alpha(alpha(x)) = x for all x in G",
    "¬Q: G is not an abelian group or alpha(x) != x^-1 for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3