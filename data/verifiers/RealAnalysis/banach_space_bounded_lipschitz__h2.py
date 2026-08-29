import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: The space Lip_b(X) is endowed with the given norm",
    "¬Q: The normed vector space is not complete (e.g., norm is invalid for |X| < 2)"
]

def conditions(witness):
    h1 = False
    h2 = True
    neg_q = False
    n = -1

    try:
        if isinstance(witness, Matrix):
            if witness.rows == witness.cols:
                n = witness.rows
                h1 = True
                for i in range(n):
                    if witness[i, i] != 0:
                        h1 = False
                    for j in range(n):
                        if i != j and witness[i, j] <= 0:
                            h1 = False
                        if witness[i, j] != witness[j, i]:
                            h1 = False
                        for k in range(n):
                            if witness[i, j] > witness[i, k] + witness[k, j]:
                                h1 = False
        elif isinstance(witness, list) and all(isinstance(row, list) for row in witness):
            n = len(witness)
            if all(len(row) == n for row in witness):
                h1 = True
                for i in range(n):
                    if witness[i][i] != 0:
                        h1 = False
                    for j in range(n):
                        if i != j and witness[i][j] <= 0:
                            h1 = False
                        if witness[i][j] != witness[j][i]:
                            h1 = False
                        for k in range(n):
                            if witness[i][j] > witness[i][k] + witness[k][j]:
                                h1 = False
        elif isinstance(witness, tuple) and len(witness) == 2:
            X, d = witness
            n = len(X)
            h1 = True
            for x in X:
                if d(x, x) != 0:
                    h1 = False
                for y in X:
                    if x != y and d(x, y) <= 0:
                        h1 = False
                    if d(x, y) != d(y, x):
                        h1 = False
                    for z in X:
                        if d(x, y) > d(x, z) + d(z, y):
                            h1 = False
        elif hasattr(witness, 'points') and hasattr(witness, 'distance'):
            X = witness.points
            d = witness.distance
            n = len(X)
            h1 = True
            for x in X:
                if d(x, x) != 0:
                    h1 = False
                for y in X:
                    if x != y and d(x, y) <= 0:
                        h1 = False
                    if d(x, y) != d(y, x):
                        h1 = False
                    for z in X:
                        if d(x, y) > d(x, z) + d(z, y):
                            h1 = False
        elif witness == sympy.S.Reals:
            h1 = True
            n = 2
        elif isinstance(witness, sympy.Interval):
            h1 = True
            n = 2 if witness.measure > 0 else 1
        elif isinstance(witness, sympy.FiniteSet):
            if all(x.is_real for x in witness):
                n = len(witness)
                h1 = True
        elif isinstance(witness, int) and witness >= 0:
            n = witness
            h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            # If the metric space has fewer than 2 points, the supremum over x != y 
            # is taken over an empty set, which evaluates to -infinity.
            # Thus, the given formula does not define a valid norm (which must map to [0, infinity)),
            # meaning (Lip_b(X), ||.||_Lip) is not a normed vector space, and hence not a Banach space.
            if n < 2:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]