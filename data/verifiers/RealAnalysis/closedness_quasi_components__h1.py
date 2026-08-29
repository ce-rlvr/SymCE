import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        try:
            X = frozenset(witness.X)
            T = {frozenset(U) for U in witness.T}
            x = witness.x
        except AttributeError:
            X = frozenset(witness[0])
            T = {frozenset(U) for U in witness[1]}
            x = witness[2]
    except Exception:
        return [False, False, False]

    try:
        try:
            Q_x = frozenset(witness.Q_x)
        except AttributeError:
            if len(witness) > 3:
                Q_x = frozenset(witness[3])
            else:
                clopens = [U for U in T if (X - U) in T]
                clopens_with_x = [U for U in clopens if x in U]
                Q_x = frozenset.intersection(*clopens_with_x) if clopens_with_x else X
    except Exception:
        Q_x = None

    # H1
    h1_ok = False
    try:
        if x in X and frozenset() in T and X in T:
            is_top = True
            for A in T:
                if not A.issubset(X):
                    is_top = False
                    break
                for B in T:
                    if A.intersection(B) not in T:
                        is_top = False
                        break
                    if A.union(B) not in T:
                        is_top = False
                        break
                if not is_top:
                    break
            h1_ok = is_top
    except Exception:
        h1_ok = False

    # H2
    h2_ok = False
    try:
        if Q_x is not None:
            clopens = [U for U in T if (X - U) in T]
            clopens_with_x = [U for U in clopens if x in U]
            expected_Q_x = frozenset.intersection(*clopens_with_x) if clopens_with_x else X
            h2_ok = (Q_x == expected_Q_x)
    except Exception:
        h2_ok = False

    # neg_Q
    neg_q_ok = False
    try:
        if Q_x is not None:
            is_closed = (X - Q_x) in T
            neg_q_ok = not is_closed
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an element of X and X is a topological space",
    "H_2: Q_x is the quasi-component of X containing x",
    "¬Q: Q_x is not a closed subset of X"
]

N_HYP = 2
NEG_Q_INDEX = 2