import sympy
from sympy import Symbol, limit_seq, limit, oo
from sympy.calculus.util import AccumBounds

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    # Evaluate witness if it's a callable
    if callable(witness):
        try:
            expr = witness(n)
        except Exception:
            return [False, False]
    else:
        expr = witness

    # Extract formula if it's a SymPy Sequence object
    if hasattr(expr, 'formula'):
        try:
            expr = expr.formula
        except Exception:
            pass

    # H_1: (a_n) is a bounded sequence of real numbers
    h1_ok = False
    try:
        # Check if the sequence is real-valued for the first few terms
        is_real = True
        for i in range(1, 6):
            try:
                val = expr.subs(n, i).evalf()
                if val.is_number and getattr(val, 'is_real', None) is False:
                    is_real = False
                    break
            except Exception:
                pass
        
        if is_real:
            bounded = False
            evaluated = False
            
            # 1. Try limit_seq
            try:
                L = limit_seq(expr, n)
                if L is not None and L is not sympy.nan:
                    evaluated = True
                    if isinstance(L, AccumBounds):
                        if L.min.is_finite and L.max.is_finite:
                            bounded = True
                    elif L.is_number and L.is_finite:
                        bounded = True
            except Exception:
                pass
            
            # 2. Try continuous limit
            if not evaluated:
                try:
                    L = limit(expr, n, oo)
                    if L is not None and L is not sympy.nan and not isinstance(L, sympy.Limit):
                        evaluated = True
                        if isinstance(L, AccumBounds):
                            if L.min.is_finite and L.max.is_finite:
                                bounded = True
                        elif L.is_number and L.is_finite:
                            bounded = True
                except Exception:
                    pass
            
            # 3. Heuristic fallback
            if not evaluated:
                try:
                    vals = [float(abs(expr.subs(n, i).evalf())) for i in range(1, 200)]
                    if max(vals) < 1e5:
                        diffs = [vals[i] - vals[i-1] for i in range(1, len(vals))]
                        if all(d > 0.1 for d in diffs[-10:]):
                            bounded = False
                        else:
                            bounded = True
                except Exception:
                    pass
            
            h1_ok = bounded
    except Exception:
        h1_ok = False

    # ¬Q: The sequence (a_n) does NOT converge to a finite real limit
    neg_q_ok = False
    try:
        converges = False
        evaluated = False
        
        # 1. Try limit_seq
        try:
            L = limit_seq(expr, n)
            if L is not None and L is not sympy.nan:
                evaluated = True
                if isinstance(L, AccumBounds):
                    if L.min == L.max and L.min.is_finite:
                        converges = True
                elif L.is_number and L.is_finite:
                    converges = True
        except Exception:
            pass
            
        # 2. Try continuous limit
        if not evaluated:
            try:
                L = limit(expr, n, oo)
                if L is not None and L is not sympy.nan and not isinstance(L, sympy.Limit):
                    evaluated = True
                    if isinstance(L, AccumBounds):
                        if L.min == L.max and L.min.is_finite:
                            converges = True
                    elif L.is_number and L.is_finite:
                        converges = True
            except Exception:
                pass
                
        # 3. Heuristic fallback
        if not evaluated:
            try:
                vals = [float(expr.subs(n, i).evalf()) for i in range(100, 150)]
                if max(vals) - min(vals) < 1e-5:
                    converges = True
            except Exception:
                pass
                
        neg_q_ok = not converges
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a_n) is a bounded sequence of real numbers",
    "¬Q: The sequence (a_n) does not converge to a finite real limit"
]

N_HYP = 1
NEG_Q_INDEX = 1