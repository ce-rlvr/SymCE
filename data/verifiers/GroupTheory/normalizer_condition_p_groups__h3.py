import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup for witness expressions
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

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Normalizer Condition for Finite p-groups.
    The witness should be a tuple (p, G, H) where:
      - p is a prime
      - G is a finite p-group
      - H is a subgroup of G
    """
    try:
        p, G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: G is a finite group of order p^n for some integer n >= 1
    try:
        order = G.order()
        if order < p:
            h2 = False
        else:
            temp = order
            while temp % p == 0:
                temp //= p
            h2 = (temp == 1)
            
        # Implicitly, H must be a subgroup of G
        if h2:
            for g in H.generators:
                if not G.contains(g):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: H is NOT strictly contained in its normalizer N_G(H)
    # This means there is NO element g in G \ H that normalizes H.
    try:
        strictly_contained = False
        for g in G.elements:
            if not H.contains(g):
                # Check if g normalizes H (i.e., g * h * g^-1 in H for all generators h of H)
                normalizes = True
                for h in H.generators:
                    if not H.contains(g * h * ~g):
                        normalizes = False
                        break
                if normalizes:
                    strictly_contained = True
                    break
        neg_q = not strictly_contained
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite group of order p^n for some integer n >= 1",
    "¬Q: H is not strictly contained in its normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2