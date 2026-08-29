import math
import itertools
import functools
import sympy
import z3
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok].
    """
    # 1. Try to use methods if the witness is a custom object designed for this domain
    if hasattr(witness, 'is_compact_metric_space_X'):
        try:
            h1 = bool(witness.is_compact_metric_space_X())
            h2 = bool(witness.is_metric_space_Y())
            h3 = bool(witness.is_equicontinuous_at_all_x())
            neg_q = not bool(witness.is_uniformly_equicontinuous())
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Try to treat witness as a dictionary or object with finite sets
    try:
        if isinstance(witness, dict):
            X = witness['X']
            Y = witness['Y']
            d_X = witness['d_X']
            d_Y = witness['d_Y']
            F = witness['F']
        else:
            X = witness.X
            Y = witness.Y
            d_X = witness.d_X
            d_Y = witness.d_Y
            F = witness.F
    except Exception:
        return [False, False, False, False]

    # Ensure the spaces and family are finite collections to guarantee termination
    if not isinstance(X, (list, tuple, set)) or not isinstance(Y, (list, tuple, set)):
        return [False, False, False, False]
    if not isinstance(F, (list, tuple, set)):
        return [False, False, False, False]

    def is_metric(space, dist):
        for x in space:
            try:
                if float(dist(x, x)) != 0.0: return False
            except Exception: return False
            for y in space:
                try:
                    d_xy = float(dist(x, y))
                    d_yx = float(dist(y, x))
                except Exception: return False
                if d_xy < 0: return False
                if x != y and d_xy == 0: return False
                if abs(d_xy - d_yx) > 1e-7: return False
                for z in space:
                    try:
                        d_xz = float(dist(x, z))
                        d_yz = float(dist(y, z))
                    except Exception: return False
                    if d_xz > d_xy + d_yz + 1e-7: return False
        return True

    try:
        h1 = is_metric(X, d_X)
        # Note: Any finite metric space is trivially compact.
    except Exception:
        h1 = False

    try:
        h2 = is_metric(Y, d_Y)
    except Exception:
        h2 = False

    try:
        h3 = True
        for f in F:
            for x in X:
                fx = f(x)
                if not any(y == fx for y in Y):
                    h3 = False
    except Exception:
        h3 = False

    try:
        # For any finite metric space, equicontinuity at every point logically implies 
        # uniform equicontinuity. Thus, the conclusion holds and its negation is False.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: Y is a metric space",
    "H_3: For every x in X, the family F is equicontinuous at x",
    "¬Q: The family F is not uniformly equicontinuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3