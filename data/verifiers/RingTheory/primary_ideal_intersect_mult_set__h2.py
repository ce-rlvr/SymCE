import sympy
from sympy import *
import itertools
import functools
import math

# Top-level setup
# Witness is expected to be a dict {'n': int, 'S': list, 'P': list, 'Q': list} 
# representing subsets of the ring Z/nZ.
# Alternatively, it can be a tuple (n, S, P, Q). 
# If n is omitted (e.g. tuple of length 3), the ring is assumed to be Z.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', None)
            S = witness.get('S', [])
            P = witness.get('P', [])
            Q = witness.get('Q', [])
        elif hasattr(witness, 'n') and hasattr(witness, 'S'):
            n = getattr(witness, 'n', None)
            S = getattr(witness, 'S', [])
            P = getattr(witness, 'P', [])
            Q = getattr(witness, 'Q', [])
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                n, S, P, Q = witness
            elif len(witness) == 3:
                S, P, Q = witness
                n = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        S = set(S)
        P = set(P)
        Q = set(Q)
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        if n is not None:
            h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
            # Verify that S, P, Q are valid subsets of Z/nZ
            if h1:
                for x in S.union(P).union(Q):
                    if not (isinstance(x, (int, sympy.Integer)) and 0 <= x < n):
                        h1 = False
                        break
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        for a in S:
            for b in S:
                prod = (a * b) % n if n is not None else (a * b)
                if prod not in S:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: S \cap P \neq \emptyset
    try:
        h3 = len(S.intersection(P)) > 0
    except Exception:
        h3 = False

    # Neg Q: S \cap Q == \emptyset
    try:
        neg_q = len(S.intersection(Q)) == 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: S intersection P is non-empty",
    "¬Q: S intersection Q is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3