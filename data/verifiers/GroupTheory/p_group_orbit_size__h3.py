import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P, X, O = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: P is a finite p-group for some prime p
    try:
        h1 = False
        if hasattr(P, 'order'):
            order = P.order()
            if order == 1:
                h1 = True
            else:
                factors = sympy.factorint(order)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                    if sympy.isprime(p):
                        h1 = True
    except Exception:
        h1 = False

    # H2: X is a finite set
    try:
        h2 = False
        if isinstance(X, (set, list, tuple)):
            h2 = True
        elif hasattr(X, 'is_FiniteSet') and X.is_FiniteSet:
            h2 = True
    except Exception:
        h2 = False

    # H3: O is an orbit of the action of P on X
    try:
        h3 = False
        if h2 and hasattr(P, 'orbits'):
            O_set = set(O)
            X_set = set(X)
            if O_set.issubset(X_set):
                for orb in P.orbits():
                    if set(orb) == O_set:
                        h3 = True
                        break
    except Exception:
        h3 = False

    # neg_Q: The cardinality of O is NOT equal to p^k for some non-negative integer k
    try:
        neg_q = False
        if hasattr(P, 'order'):
            order = P.order()
            if order == 1:
                p = 2
            else:
                factors = sympy.factorint(order)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                else:
                    p = None
            
            if p is not None:
                size = len(O)
                if size == 0:
                    neg_q = True
                else:
                    temp = size
                    while temp % p == 0:
                        temp //= p
                    neg_q = (temp != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a finite p-group for some prime p",
    "H_2: X is a finite set",
    "H_3: O is an orbit of the action of P on X",
    "¬Q: The cardinality of O is not equal to p^k for any non-negative integer k"
]

N_HYP = 3
NEG_Q_INDEX = 3