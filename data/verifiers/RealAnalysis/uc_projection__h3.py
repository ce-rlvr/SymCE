import itertools
import math
import sympy
from sympy import Interval, S, Set

# Top-level setup
# No specific named objects required for this domain

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'X1'):
            X1 = witness.X1
            d1 = witness.d1
            X2 = witness.X2
            d2 = witness.d2
            d = getattr(witness, 'd', None)
        elif isinstance(witness, dict):
            if 'X1' not in witness or 'd1' not in witness or 'X2' not in witness or 'd2' not in witness:
                return [False, False, False]
            X1 = witness['X1']
            d1 = witness['d1']
            X2 = witness['X2']
            d2 = witness['d2']
            d = witness.get('d')
        else:
            if len(witness) < 4:
                return [False, False, False]
            X1, d1, X2, d2 = witness[:4]
            d = witness[4] if len(witness) > 4 else None
    except Exception:
        return [False, False, False]

    def get_points(X):
        try:
            return list(itertools.islice(X, 50))
        except TypeError:
            if isinstance(X, Interval):
                pts = []
                if X.inf.is_finite and X.sup.is_finite:
                    pts = [X.inf, X.sup, (X.inf + X.sup)/2]
                elif X.inf.is_finite:
                    pts = [X.inf, X.inf + 1, X.inf + 2]
                elif X.sup.is_finite:
                    pts = [X.sup, X.sup - 1, X.sup - 2]
                else:
                    pts = [S(0), S(1), S(-1)]
                return [p for p in pts if X.contains(p)]
            elif isinstance(X, Set):
                return []
            raise

    def is_metric(X, dist):
        try:
            points = get_points(X)
            if not points:
                if isinstance(X, Set) and X.is_empty:
                    return True
                if not isinstance(X, Set):
                    return True
            for x in points:
                for y in points:
                    d_xy = float(dist(x, y))
                    if not math.isfinite(d_xy): return False
                    if d_xy < -1e-7: return False
                    if x == y:
                        if d_xy > 1e-7: return False
                    else:
                        if d_xy <= 1e-7: return False
                    d_yx = float(dist(y, x))
                    if abs(d_xy - d_yx) > 1e-7: return False
                    for z in points:
                        d_xz = float(dist(x, z))
                        d_yz = float(dist(y, z))
                        if d_xz > d_xy + d_yz + 1e-7: return False
            return True
        except Exception:
            return False

    h1 = is_metric(X1, d1) and is_metric(X2, d2)

    if d is None:
        d = lambda x, y: d1(x[0], y[0]) + d2(x[1], y[1])

    def check_sum_metric(X1, d1, X2, d2, d):
        try:
            pts1 = get_points(X1)[:10]
            pts2 = get_points(X2)[:10]
            if not pts1 or not pts2:
                return True
            for x1 in pts1:
                for x2 in pts2:
                    for y1 in pts1:
                        for y2 in pts2:
                            expected = float(d1(x1, y1)) + float(d2(x2, y2))
                            actual = float(d((x1, x2), (y1, y2)))
                            if not math.isfinite(actual) or abs(expected - actual) > 1e-7:
                                return False
            return True
        except Exception:
            return False

    h2 = check_sum_metric(X1, d1, X2, d2, d)

    neg_q = False
    try:
        if hasattr(witness, 'is_uniformly_continuous'):
            neg_q = not witness.is_uniformly_continuous()
        elif isinstance(witness, dict) and 'is_uniformly_continuous' in witness:
            val = witness['is_uniformly_continuous']
            neg_q = not (val() if callable(val) else val)
        elif isinstance(witness, dict) and 'seq_x' in witness and 'seq_y' in witness and 'epsilon' in witness:
            epsilon = float(witness['epsilon'])
            seq_x = witness['seq_x']
            seq_y = witness['seq_y']
            
            violates_uniform_continuity = True
            for n in range(10):
                x = seq_x(n) if callable(seq_x) else seq_x[n]
                y = seq_y(n) if callable(seq_y) else seq_y[n]
                
                dist_xy = float(d(x, y))
                dist_pi = float(d1(x[0], y[0]))
                
                if dist_pi < epsilon - 1e-7:
                    violates_uniform_continuity = False
                    break
            
            if violates_uniform_continuity:
                x_last = seq_x(9) if callable(seq_x) else seq_x[9]
                y_last = seq_y(9) if callable(seq_y) else seq_y[9]
                if float(d(x_last, y_last)) < 1e-2:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X_1, d_1) and (X_2, d_2) are metric spaces",
    "H_2: X_1 x X_2 is equipped with the sum metric",
    "¬Q: The projection map pi_1 is not uniformly continuous on X_1 x X_2"
]

N_HYP = 2
NEG_Q_INDEX = 2