import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]

    def get_phi(x):
        if callable(phi):
            return phi(x)
        return phi[x]

    # H_1: G is a finite group
    try:
        elements = list(G.elements)
        h1 = len(elements) > 0 and hasattr(G, 'is_abelian')
    except Exception:
        h1 = False

    # H_2: \phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            images = []
            h2 = True
            for x in elements:
                px = get_phi(x)
                if px not in elements:
                    h2 = False
                    break
                images.append(px)
            
            if h2:
                # Check bijection
                if len(set(images)) != len(elements):
                    h2 = False
                else:
                    # Check homomorphism
                    for x in elements:
                        for y in elements:
                            if get_phi(x * y) != get_phi(x) * get_phi(y):
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: \phi(\phi(x)) = x for all x \in G
    try:
        if not h1 or not h2:
            h3 = False
        else:
            h3 = True
            for x in elements:
                if get_phi(get_phi(x)) != x:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: G is not abelian or \phi(x) != x^{-1} for some x \in G
    try:
        if not h1:
            neg_q = False
        else:
            is_abelian = bool(getattr(G, 'is_abelian', False))
            is_inversion = True
            for x in elements:
                inv_x = ~x if hasattr(x, '__invert__') else x**-1
                if get_phi(x) != inv_x:
                    is_inversion = False
                    break
            neg_q = not (is_abelian and is_inversion)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\phi is an automorphism of G",
    "H_3: \\phi(\\phi(x)) = x for all x \\in G",
    "¬Q: G is not abelian or \\phi(x) != x^{-1} for some x \\in G"
]

N_HYP = 3
NEG_Q_INDEX = 3