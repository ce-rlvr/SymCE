import sympy
import math

def conditions(witness):
    n = sympy.Symbol('n', integer=True, positive=True)
    
    if callable(witness):
        try:
            expr = witness(n)
        except Exception:
            expr = None
        def a(k):
            return witness(k)
    else:
        expr = witness
        def a(k):
            return expr.subs(n, k)
            
    # H_1: a_n = H_n for all n >= 1
    h1 = True
    try:
        for k in range(1, 20):
            val = a(k)
            expected = sympy.harmonic(k)
            diff = sympy.simplify(val - expected)
            if diff != 0:
                try:
                    if abs(float(diff)) > 1e-9:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # neg_Q: Radius of convergence is NOT exactly 1
    neg_q = False
    
    def check_numerical(a_func):
        try:
            val = sympy.Abs(a_func(50000))
            if val == 0:
                return True
            log_val = float(sympy.log(val))
            log_root = log_val / 50000
            if abs(log_root) > 0.05:
                return True
            return False
        except Exception:
            return True

    try:
        if expr is not None:
            # Try root test limit
            root = sympy.Abs(expr)**(1/n)
            L_root = sympy.limit(root, n, sympy.oo)
            if not isinstance(L_root, sympy.Limit):
                if L_root != 1:
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Try ratio test limit
                ratio = sympy.Abs(expr.subs(n, n+1) / expr)
                L_ratio = sympy.limit(ratio, n, sympy.oo)
                if not isinstance(L_ratio, sympy.Limit):
                    if L_ratio != 1:
                        neg_q = True
                    else:
                        neg_q = False
                else:
                    neg_q = check_numerical(a)
        else:
            neg_q = check_numerical(a)
    except Exception:
        neg_q = check_numerical(a)
            
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_n = H_n for all integers n >= 1",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1