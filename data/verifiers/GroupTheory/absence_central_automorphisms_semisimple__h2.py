import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def apply_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    return alpha(g)

def conditions(witness) -> list[bool]:
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.generate())
            h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H_2: alpha is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            images = []
            h2 = True
            for g in elements:
                img = apply_alpha(alpha, g)
                if img not in elements:
                    h2 = False
                    break
                images.append(img)
            
            if h2:
                if len(set(images)) != len(elements):
                    h2 = False
                else:
                    for g in elements:
                        for h in elements:
                            if apply_alpha(alpha, g * h) != apply_alpha(alpha, g) * apply_alpha(alpha, h):
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: For all g in G, g^{-1}*alpha(g) belongs to the center of G
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            for g in elements:
                z = (g**-1) * apply_alpha(alpha, g)
                for x in elements:
                    if z * x != x * z:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: alpha is not the identity automorphism on G
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = False
            for g in elements:
                if apply_alpha(alpha, g) != g:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha is an automorphism of G",
    "H_3: For all g in G, g^{-1}*alpha(g) belongs to the center of G",
    "¬Q: The automorphism alpha is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3