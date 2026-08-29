import sympy
from sympy import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Arzelà-Ascoli conjecture.
    The witness should provide:
      - X: a finite list of points (representing a compact metric space)
      - d_X: metric on X
      - f: function f(n, x) representing the sequence of functions
      - d_Y: metric on the target space Y
      - origin_Y: (optional) a reference point in Y to check boundedness
    """
    # Extract components
    try:
        if isinstance(witness, dict):
            X = witness['X']
            d_X = witness['d_X']
            f = witness['f']
            d_Y = witness['d_Y']
            origin_Y = witness.get('origin_Y', f(1, X[0]))
        else:
            X = witness.X
            d_X = witness.d_X
            f = witness.f
            d_Y = witness.d_Y
            origin_Y = getattr(witness, 'origin_Y', f(1, X[0]))
    except Exception:
        return [False, False, False, False]

    # H1: X is a compact metric space
    # A finite metric space is always compact. We verify it is a valid finite metric space.
    h1 = False
    try:
        if isinstance(X, list) and len(X) > 0:
            is_metric = True
            for x in X:
                if abs(float(d_X(x, x))) > 1e-9: 
                    is_metric = False
                for y in X:
                    d_xy = float(d_X(x, y))
                    d_yx = float(d_X(y, x))
                    if d_xy < -1e-9: 
                        is_metric = False
                    if abs(d_xy - d_yx) > 1e-9: 
                        is_metric = False
                    for z in X:
                        d_xz = float(d_X(x, z))
                        d_yz = float(d_X(y, z))
                        if d_xz > d_xy + d_yz + 1e-9:
                            is_metric = False
            h1 = is_metric
    except Exception:
        pass

    # H2: The sequence {f_n} is pointwise bounded on X
    h2 = False
    try:
        is_pt_bounded = True
        # Check boundedness for each x up to a large n to catch unbounded sequences
        test_ns = list(range(1, 51)) + [100, 1000, 10000]
        for x in X:
            distances = [float(d_Y(f(n, x), origin_Y)) for n in test_ns]
            if max(distances) > 5000:
                is_pt_bounded = False
        
        # Verify d_Y is a valid metric on the image of f
        points_Y = [f(n, x) for n in range(1, 20) for x in X]
        is_metric_Y = True
        for y1 in points_Y[:10]:
            if abs(float(d_Y(y1, y1))) > 1e-9: 
                is_metric_Y = False
            for y2 in points_Y[:10]:
                d_y1y2 = float(d_Y(y1, y2))
                d_y2y1 = float(d_Y(y2, y1))
                if d_y1y2 < -1e-9: 
                    is_metric_Y = False
                if abs(d_y1y2 - d_y2y1) > 1e-9: 
                    is_metric_Y = False
                for y3 in points_Y[:10]:
                    d_y1y3 = float(d_Y(y1, y3))
                    d_y2y3 = float(d_Y(y2, y3))
                    if d_y1y3 > d_y1y2 + d_y2y3 + 1e-9:
                        is_metric_Y = False
        if not is_metric_Y:
            is_pt_bounded = False
            
        h2 = is_pt_bounded
    except Exception:
        pass

    # H3: The sequence {f_n} is equicontinuous on X
    h3 = False
    try:
        if len(X) == 1:
            h3 = True
        else:
            # For a finite metric space, any sequence of functions is equicontinuous 
            # provided the space is discrete (minimum distance between distinct points > 0).
            min_dist = min(float(d_X(x, y)) for x in X for y in X if x != y)
            if min_dist > 1e-9:
                h3 = True
    except Exception:
        pass

    # neg_Q: The sequence {f_n} does NOT contain a uniformly convergent subsequence
    # We verify this by checking that the sequence has no uniformly Cauchy subsequence.
    # If all pairwise distances between distinct functions are bounded away from 0, 
    # no subsequence can be Cauchy.
    neg_q = False
    try:
        eps = 1e-3
        pairwise_large = True
        for n in range(1, 51):
            for m in range(n + 1, 51):
                sup_dist = max(float(d_Y(f(n, x), f(m, x))) for x in X)
                if sup_dist < eps:
                    pairwise_large = False
                    break
            if not pairwise_large:
                break
        neg_q = pairwise_large
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: The sequence {f_n} is pointwise bounded on X",
    "H_3: The sequence {f_n} is equicontinuous on X",
    "¬Q: The sequence {f_n} does NOT contain a uniformly convergent subsequence"
]

N_HYP = 3
NEG_Q_INDEX = 3