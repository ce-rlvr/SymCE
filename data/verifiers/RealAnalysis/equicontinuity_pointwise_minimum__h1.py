import sympy
import itertools
from sympy import Symbol, Interval, oo

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    # If the witness provides its own evaluation logic, use it.
    if hasattr(witness, 'evaluate') and callable(witness.evaluate):
        try:
            return witness.evaluate()
        except Exception:
            pass

    try:
        if isinstance(witness, dict):
            F = witness.get('F', [])
            M = witness.get('M', [])
            X = witness.get('X', [])
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            F, M, X = witness
        else:
            F = getattr(witness, 'F', [])
            M = getattr(witness, 'M', [])
            X = getattr(witness, 'X', [])
            
        if not F or not M or X is None:
            return [False, False, False]
            
        if isinstance(X, Interval):
            start = float(X.start) if X.start != -oo else -10.0
            end = float(X.end) if X.end != oo else 10.0
            X_pts = [start + i * (end - start) / 20.0 for i in range(21)]
        elif not isinstance(X, (list, tuple)):
            X_pts = list(X)
        else:
            X_pts = X
            
    except Exception:
        return [False, False, False]

    def evaluate_f(f, x_val):
        if callable(f):
            return float(f(x_val))
        else:
            if hasattr(f, 'free_symbols'):
                syms = list(f.free_symbols)
                if len(syms) == 1:
                    return float(f.subs(syms[0], x_val))
                elif len(syms) == 0:
                    return float(f)
                else:
                    raise ValueError("Too many free symbols")
            else:
                return float(f)

    def is_equicontinuous(family, pts):
        if not family:
            return True
        L_max = 0.0
        for f in family:
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    dx = abs(pts[i] - pts[j])
                    if dx > 1e-9:
                        dy = abs(evaluate_f(f, pts[i]) - evaluate_f(f, pts[j]))
                        L = dy / dx
                        if L > L_max:
                            L_max = L
        return L_max < 1e4

    try:
        h1 = is_equicontinuous(F, X_pts)
    except Exception:
        h1 = False

    try:
        if len(F) > 10:
            h2 = False
        else:
            expected_M = []
            for r in range(1, len(F) + 1):
                for subset in itertools.combinations(F, r):
                    def make_min_func(sub):
                        return lambda val: min(evaluate_f(f, val) for f in sub)
                    expected_M.append(make_min_func(subset))
            
            def is_equiv(f1, f2):
                return all(abs(evaluate_f(f1, pt) - evaluate_f(f2, pt)) < 1e-6 for pt in X_pts)
            
            h2 = True
            for m in M:
                if not any(is_equiv(m, e) for e in expected_M):
                    h2 = False
                    break
            if h2:
                for e in expected_M:
                    if not any(is_equiv(e, m) for m in M):
                        h2 = False
                        break
    except Exception:
        h2 = False

    try:
        neg_q = not is_equicontinuous(M, X_pts)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is an equicontinuous family of real-valued functions on X",
    "H_2: M is the family of functions formed by taking the pointwise minimum of any finite subset of functions in F",
    "¬Q: M is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2