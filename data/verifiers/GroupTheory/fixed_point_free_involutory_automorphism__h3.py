import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
import math

# Top-level setup for potential witness expressions
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

def apply_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha[x]
    elif callable(alpha):
        return alpha(x)
    else:
        raise ValueError("alpha must be a dict or callable")

def conditions(witness):
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: \alpha is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.generate())
            mapped_elements = set()
            is_homomorphism = True
            for x in elements:
                ax = apply_alpha(alpha, x)
                if ax not in G:
                    is_homomorphism = False
                    break
                mapped_elements.add(ax)
            
            if is_homomorphism and len(mapped_elements) == len(elements):
                for x in elements:
                    for y in elements:
                        if apply_alpha(alpha, x * y) != apply_alpha(alpha, x) * apply_alpha(alpha, y):
                            is_homomorphism = False
                            break
                    if not is_homomorphism:
                        break
                h2 = is_homomorphism
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: For all x \in G, \alpha(x) = x implies x = e
    try:
        if not h1:
            h3 = False
        else:
            elements = list(G.generate())
            h3 = True
            for x in elements:
                if apply_alpha(alpha, x) == x:
                    if x != G.identity:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: G is not abelian OR \alpha(x) != x^{-1} for some x
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.generate())
            is_abelian = G.is_abelian
            
            inv_property = True
            for x in elements:
                if apply_alpha(alpha, x) != x**-1:
                    inv_property = False
                    break
            
            neg_q = not (is_abelian and inv_property)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha is an automorphism of G",
    "H_3: For all x in G, alpha(x) = x implies x = e",
    "¬Q: G is not abelian or alpha(x) != x^-1 for some x"
]

N_HYP = 3
NEG_Q_INDEX = 3