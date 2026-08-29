import sympy
from sympy import Symbol, diff, solve, limit, oo

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        # Handle both callable functions and sympy expressions
        if callable(witness):
            try:
                expr = witness(n, x)
            except Exception:
                expr = witness
        else:
            expr = witness

        # We want to check if the sequence of functions (expr) 
        # does NOT converge uniformly to 0 on R.
        # This means lim_{n->oo} sup_{x} |expr(x)| != 0.
        
        # First, try to find critical points to locate the supremum
        try:
            df = diff(expr, x)
            cps = solve(df, x)
        except Exception:
            cps = []
            
        # Also add some common test points that might witness non-uniform convergence
        test_points = [
            1/n, -1/n, 
            1/sympy.sqrt(n), -1/sympy.sqrt(n), 
            1/n**2, -1/n**2, 
            n, -n, 
            sympy.Integer(1), sympy.Integer(-1), 
            sympy.Integer(0)
        ]
        
        points_to_check = cps + test_points
        
        for cp in points_to_check:
            try:
                val = expr.subs(x, cp)
                L = limit(val, n, oo)
                # If the limit at any of these moving points is non-zero, 
                # the convergence is not uniform to 0.
                if L != 0:
                    neg_q = True
                    break
            except Exception:
                continue
                
        # Check limits at infinity
        if not neg_q:
            try:
                L_inf = limit(expr, x, oo)
                if limit(L_inf, n, oo) != 0:
                    neg_q = True
            except Exception:
                pass
                
        if not neg_q:
            try:
                L_minf = limit(expr, x, -oo)
                if limit(L_minf, n, oo) != 0:
                    neg_q = True
            except Exception:
                pass

    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The sequence (f_n) does not converge uniformly to the zero function on R"
]

N_HYP = 0
NEG_Q_INDEX = 0