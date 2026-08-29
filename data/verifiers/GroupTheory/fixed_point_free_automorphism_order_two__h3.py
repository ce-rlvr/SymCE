import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
import math

# Top-level setup
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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
            
            e = None
            for x in elements:
                if x * x == x:
                    e = x
                    break
            if e is None:
                h1 = False
    except Exception:
        h1 = False

    def apply_phi(x):
        if callable(phi):
            return phi(x)
        elif isinstance(phi, dict):
            return phi.get(x, None)
        else:
            return None

    # H2: phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            mapped_elements = []
            h2 = True
            for x in elements:
                px = apply_phi(x)
                if px not in elements:
                    h2 = False
                    break
                mapped_elements.append(px)
            if h2:
                if len(set(mapped_elements)) != len(elements):
                    h2 = False
            if h2:
                for x in elements:
                    for y in elements:
                        if apply_phi(x * y) != apply_phi(x) * apply_phi(y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: phi(x) = x implies x = e
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            for x in elements:
                if apply_phi(x) == x:
                    if x != e:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: G is not abelian OR phi(x) != x^-1 for some x
    try:
        if not h1:
            neg_q = False
        else:
            is_abelian = True
            for x in elements:
                for y in elements:
                    if x * y != y * x:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            
            phi_is_inversion = True
            for x in elements:
                if apply_phi(x) != x**-1:
                    phi_is_inversion = False
                    break
            
            neg_q = (not is_abelian) or (not phi_is_inversion)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\phi is an automorphism of G",
    "H_3: \\phi(x) = x implies x = e",
    "¬Q: G is not abelian or \\phi(x) != x^{-1} for some x"
]

N_HYP = 3
NEG_Q_INDEX = 3