import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Standard algebra objects
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
        X = witness['X']
        d = witness['d']
        K = witness['K']
        x = witness['x']
    except Exception:
        return [False, False, False]
        
    try:
        X_list = list(X)
    except Exception:
        X_list = []
        
    try:
        K_list = list(K)
    except Exception:
        K_list = []

    # H1: (X, d) is a metric space
    h1 = False
    try:
        if len(X_list) > 0:
            is_metric = True
            for a in X_list:
                for b in X_list:
                    dist_ab = float(d(a, b))
                    if a == b:
                        if dist_ab != 0:
                            is_metric = False
                    else:
                        if dist_ab <= 1e-12:
                            is_metric = False
                    
                    if abs(dist_ab - float(d(b, a))) > 1e-12:
                        is_metric = False
                        
                    for c in X_list:
                        dac = float(d(a, c))
                        dbc = float(d(b, c))
                        if dac > dist_ab + dbc + 1e-9:
                            is_metric = False
            h1 = is_metric
    except Exception:
        h1 = False

    # H2: K is a non-empty sequentially compact subset of X
    h2 = False
    try:
        if len(K_list) > 0:
            if all(k in X_list for k in K_list):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    neg_q = False
    try:
        if len(K_list) == 0:
            neg_q = True
        else:
            distances = []
            for z in K_list:
                distances.append(float(d(x, z)))
            inf_d = min(distances)
            q = False
            for y in K_list:
                if abs(float(d(x, y)) - inf_d) < 1e-9:
                    q = True
                    break
            neg_q = not q
    except Exception:
        # If d(x, z) is undefined or raises an error (e.g., x is not in X), the conclusion fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: K is a non-empty sequentially compact subset of X",
    "¬Q: There does not exist y in K such that d(x, y) = inf_{z in K} d(x, z)"
]

N_HYP = 2
NEG_Q_INDEX = 2