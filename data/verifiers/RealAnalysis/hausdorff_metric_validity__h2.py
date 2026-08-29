import itertools
import math
import sympy
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    """
    Parses the witness into a list of points and a distance function.
    Supports distance matrices, lists of points (1D), tuples of (points, d), etc.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        points, d = witness
        return list(points), lambda x, y: float(d(x, y))
    elif isinstance(witness, list) and all(isinstance(row, list) for row in witness):
        n = len(witness)
        points = list(range(n))
        d = lambda x, y: float(witness[x][y])
        return points, d
    elif isinstance(witness, list) and all(isinstance(x, (int, float, sympy.Basic)) for x in witness):
        points = witness
        d = lambda x, y: float(abs(x - y))
        return points, d
    elif hasattr(witness, 'points') and hasattr(witness, 'd'):
        return list(witness.points), lambda x, y: float(witness.d(x, y))
    elif isinstance(witness, int) and witness > 0:
        points = list(range(witness))
        d = lambda x, y: float(abs(x - y))
        return points, d
    else:
        raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    # H_1: (X, d) is a metric space
    try:
        points, d = parse_witness(witness)
        n = len(points)
        # Limit size to prevent combinatorial explosion in K(X) checks
        if n == 0 or n > 5:
            h1 = False
        else:
            is_metric = True
            for i in points:
                for j in points:
                    try:
                        dist = d(i, j)
                        if dist < 0:
                            is_metric = False
                        if i == j and dist != 0:
                            is_metric = False
                        if i != j and dist == 0:
                            is_metric = False
                        if abs(dist - d(j, i)) > 1e-9:
                            is_metric = False
                    except Exception:
                        is_metric = False
            
            for i in points:
                for j in points:
                    for k in points:
                        try:
                            if d(i, k) > d(i, j) + d(j, k) + 1e-9:
                                is_metric = False
                        except Exception:
                            is_metric = False
            h1 = is_metric
    except Exception:
        h1 = False

    # H_2: d_H is the Hausdorff distance defined by the standard formula
    # This is a definitional hypothesis, so it holds if the space is valid.
    h2 = h1

    # ¬Q: (K(X), d_H) is NOT a metric space
    try:
        if not h1:
            neg_q = False
        else:
            # K(X) is the set of all compact subsets. For a finite space, it's the power set.
            K_X = []
            for r in range(n + 1):
                for combo in itertools.combinations(points, r):
                    K_X.append(frozenset(combo))
            
            def d_H(A, B):
                if not A and not B:
                    return float('-inf')
                if not A or not B:
                    return float('inf')
                
                def dist_point_set(x, S):
                    return min(d(x, y) for y in S)
                
                sup_A = max(dist_point_set(a, B) for a in A)
                sup_B = max(dist_point_set(b, A) for b in B)
                return max(sup_A, sup_B)
            
            is_metric_space = True
            for A in K_X:
                for B in K_X:
                    d_val = d_H(A, B)
                    if math.isinf(d_val) or math.isnan(d_val):
                        is_metric_space = False
                    elif d_val < 0:
                        is_metric_space = False
                    elif (abs(d_val) < 1e-9) != (A == B):
                        is_metric_space = False
                    
                    if not is_metric_space:
                        break
                if not is_metric_space:
                    break
            
            if is_metric_space:
                for A in K_X:
                    for B in K_X:
                        for C in K_X:
                            if d_H(A, C) > d_H(A, B) + d_H(B, C) + 1e-9:
                                is_metric_space = False
                                break
                        if not is_metric_space:
                            break
                    if not is_metric_space:
                        break
            
            neg_q = not is_metric_space
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: d_H is the Hausdorff distance",
    "¬Q: (K(X), d_H) is not a metric space"
]

N_HYP = 2
NEG_Q_INDEX = 2