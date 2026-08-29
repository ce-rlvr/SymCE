import sympy
from sympy import S
import math

# Top-level setup for common mathematical objects
R = S.Reals
Z = S.Integers
N = S.Naturals
Q = S.Rationals

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X is not totally bounded (cannot be covered by finitely many balls of some radius epsilon)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If (X, d) is a metric space, then X is totally bounded."
    
    The witness should represent an infinite metric space that is not totally bounded.
    Expected witness formats:
      - (X, d)
      - (X, d, epsilon)
      - (X, d, epsilon, sequence)
    where X is the space (e.g., S.Reals), d is the metric function, epsilon is a positive float,
    and sequence is an iterable or callable generating points in X.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                X, d = witness
                epsilon = 1.0
                seq = list(range(200))
            elif len(witness) == 3:
                try:
                    epsilon = float(witness[2])
                    X, d = witness[:2]
                    seq = list(range(200))
                except Exception:
                    X, d, seq = witness
                    epsilon = 1.0
            elif len(witness) >= 4:
                X, d, epsilon, seq = witness[:4]
                epsilon = float(epsilon)
            else:
                return [False, False]
        else:
            return [False, False]
            
        if callable(seq):
            try:
                seq_pts = [seq(i) for i in range(200)]
            except Exception:
                seq_pts = []
        else:
            seq_pts = list(seq)
            
        if len(seq_pts) < 50:
            seq_pts.extend(list(range(200)))
            
    except Exception:
        return [False, False]

    # H_1: (X, d) is a metric space
    h1_ok = False
    try:
        sample_points = []
        for pt in seq_pts:
            if pt not in sample_points:
                sample_points.append(pt)
            if len(sample_points) >= 20:
                break
                
        if hasattr(X, 'contains'):
            for p in [0, 1, 2, 0.5, -1, sympy.pi]:
                try:
                    res = X.contains(p)
                    if isinstance(res, sympy.Basic):
                        res = bool(res)
                    if res and p not in sample_points:
                        sample_points.append(p)
                except Exception:
                    pass
        
        if len(sample_points) < 3:
            h1_ok = False
        else:
            is_metric = True
            for x in sample_points:
                for y in sample_points:
                    dist_xy = float(d(x, y))
                    
                    # Non-negativity
                    if dist_xy < -1e-12:
                        is_metric = False
                        break
                        
                    # Identity of indiscernibles
                    eq = (x == y)
                    if isinstance(eq, sympy.Basic):
                        eq = bool(eq)
                    if (dist_xy < 1e-12) != eq:
                        is_metric = False
                        break
                        
                    # Symmetry
                    dist_yx = float(d(y, x))
                    if not math.isclose(dist_xy, dist_yx, rel_tol=1e-5, abs_tol=1e-9):
                        is_metric = False
                        break
                        
                    # Triangle inequality
                    for z in sample_points:
                        dist_xz = float(d(x, z))
                        dist_yz = float(d(y, z))
                        if dist_xz > dist_xy + dist_yz + 1e-7:
                            is_metric = False
                            break
                            
                if not is_metric:
                    break
            h1_ok = is_metric
    except Exception:
        h1_ok = False

    # ¬Q: X is not totally bounded
    neg_q_ok = False
    try:
        is_finite = False
        if isinstance(X, (list, tuple, set, frozenset, dict)):
            is_finite = True
        elif hasattr(X, 'is_finite'):
            try:
                is_finite = bool(X.is_finite)
            except Exception:
                pass
            
        if is_finite:
            neg_q_ok = False
        elif epsilon <= 0:
            neg_q_ok = False
        else:
            valid_seq = []
            for pt in seq_pts:
                in_X = True
                try:
                    if hasattr(X, 'contains'):
                        res = X.contains(pt)
                        if isinstance(res, sympy.Basic):
                            in_X = bool(res)
                        else:
                            in_X = bool(res)
                    elif hasattr(X, '__contains__'):
                        in_X = pt in X
                except Exception:
                    pass
                    
                if in_X:
                    valid_seq.append(pt)
                    
            # To heuristically prove it's not totally bounded, we look for a large number 
            # of points (e.g., 40) that are mutually separated by at least epsilon.
            if len(valid_seq) >= 40:
                separated = True
                check_pts = valid_seq[:40]
                for i in range(len(check_pts)):
                    for j in range(i+1, len(check_pts)):
                        if float(d(check_pts[i], check_pts[j])) < epsilon - 1e-7:
                            separated = False
                            break
                    if not separated:
                        break
                neg_q_ok = separated
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]