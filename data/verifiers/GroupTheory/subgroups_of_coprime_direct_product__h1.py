import math
import itertools
import functools
import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_order(X):
    if hasattr(X, 'order'):
        try:
            return int(X.order())
        except Exception:
            pass
    if hasattr(X, 'elements'):
        try:
            return len(list(X.elements))
        except Exception:
            pass
    if hasattr(X, 'generate'):
        try:
            return len(list(X.generate()))
        except Exception:
            pass
    return len(X)

def get_elements(X):
    if hasattr(X, 'elements'):
        try:
            return set(X.elements)
        except Exception:
            pass
    if hasattr(X, 'generate'):
        try:
            return set(X.generate())
        except Exception:
            pass
    return set(X)

def conditions(witness) -> list[bool]:
    """
    witness: A tuple (G, H, S) where G and H are groups (or subsets) and S is a collection of pairs.
    """
    try:
        G, H, S = witness
    except Exception:
        return [False, False, False]

    # H_1: The greatest common divisor of the order of G and the order of H is 1
    try:
        order_G = get_order(G)
        order_H = get_order(H)
        h1 = (math.gcd(order_G, order_H) == 1)
    except Exception:
        h1 = False

    # H_2: S is a subgroup of G x H
    try:
        S_set = set(S)
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        # Check if S is a subset of G x H
        is_subset = all(s[0] in G_elems and s[1] in H_elems for s in S_set)
        
        # Check if S is a group (non-empty and closed under pairwise multiplication)
        is_group = len(S_set) > 0
        if is_group:
            for x in S_set:
                for y in S_set:
                    prod = (x[0] * y[0], x[1] * y[1])
                    if prod not in S_set:
                        is_group = False
                        break
                if not is_group:
                    break
                    
        h2 = is_subset and is_group
    except Exception:
        h2 = False

    # neg_Q: S is NOT of the form A x B for any subgroup A of G and B of H
    try:
        S_set = set(S)
        # If S = A x B, then A must be exactly the projection of S onto the first coordinate,
        # and B must be exactly the projection of S onto the second coordinate.
        A_S = set(s[0] for s in S_set)
        B_S = set(s[1] for s in S_set)
        
        # S is of the form A x B if and only if its size is |A_S| * |B_S|
        is_A_x_B = (len(S_set) == len(A_S) * len(B_S))
        
        neg_q = not is_A_x_B
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The greatest common divisor of the order of G and the order of H is 1",
    "H_2: S is a subgroup of G x H",
    "not Q: S is not of the form A x B for any subgroup A of G and B of H"
]

N_HYP = 2
NEG_Q_INDEX = 2