import sympy
from sympy.combinatorics import PermutationGroup
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
        if isinstance(witness, tuple):
            if len(witness) == 4:
                X, P, O, p = witness
            elif len(witness) == 3:
                P, O, p = witness
                X = set(range(P.degree)) if hasattr(P, 'degree') else None
            elif len(witness) == 2:
                P, O = witness
                X = set(range(P.degree)) if hasattr(P, 'degree') else None
                p = 2
            else:
                X, P, O, p = None, None, None, None
        elif isinstance(witness, dict):
            X = witness.get('X')
            P = witness.get('P')
            O = witness.get('O')
            p = witness.get('p', 2)
            if X is None and hasattr(P, 'degree'):
                X = set(range(P.degree))
        else:
            X, P, O, p = None, None, None, None
    except Exception:
        X, P, O, p = None, None, None, None

    # H1: X is a finite set
    try:
        h1 = False
        if X is not None:
            _ = len(X)
            h1 = True
    except Exception:
        h1 = False

    # H2: P acts on X
    try:
        h2 = False
        if isinstance(P, PermutationGroup) and X is not None:
            X_set = set(X)
            if set(range(P.degree)).issubset(X_set):
                h2 = True
    except Exception:
        h2 = False

    # H3: O is an orbit of the action of P on X
    try:
        h3 = False
        if h2 and O is not None:
            orbits = P.orbits()
            O_set = set(O)
            if O_set in orbits:
                h3 = True
    except Exception:
        h3 = False

    # NegQ: The cardinality of O is not equal to p^k for some non-negative integer k
    try:
        neg_q = False
        if O is not None and p is not None:
            size = len(set(O))
            is_power = False
            if size == 1:
                is_power = True
            elif size > 1:
                p_val = int(p)
                if p_val > 1:
                    temp = size
                    while temp % p_val == 0:
                        temp //= p_val
                    if temp == 1:
                        is_power = True
            neg_q = not is_power
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: P acts on X",
    "H_3: O is an orbit of the action of P on X",
    "¬Q: The cardinality of O is not equal to p^k for some non-negative integer k"
]

N_HYP = 3
NEG_Q_INDEX = 3