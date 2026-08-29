import sympy
import math

# No named bindings needed for Number Theory; use integers directly.

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        
        # Fast path for positive integers where the identity is known to hold
        if n.is_Integer and n.is_positive:
            n_int = int(n)
            if n_int > 100000:
                return [False]
            lhs = sum(sympy.divisor_sigma(m) for m in range(1, n_int + 1))
            rhs = sum(m * (n_int // m) for m in range(1, n_int + 1))
            neg_Q = bool(lhs != rhs)
            return [neg_Q]
            
        # Fallback for non-positive integers, floats, or symbolic expressions
        m = sympy.Symbol('m', integer=True)
        lhs_expr = sympy.Sum(sympy.divisor_sigma(m), (m, 1, n))
        rhs_expr = sympy.Sum(m * sympy.floor(n/m), (m, 1, n))
        
        lhs = lhs_expr.doit()
        rhs = rhs_expr.doit()
        
        if hasattr(lhs, 'is_Integer') and lhs.is_Integer and hasattr(rhs, 'is_Integer') and rhs.is_Integer:
            neg_Q = bool(lhs != rhs)
        else:
            try:
                lhs_val = float(lhs)
                rhs_val = float(rhs)
                neg_Q = not math.isclose(lhs_val, rhs_val, rel_tol=1e-9)
            except Exception:
                # If it cannot be evaluated to a float (e.g., unevaluated sum or division by zero),
                # the identity fails to hold strictly.
                neg_Q = True
    except Exception:
        neg_Q = True
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: \\sum_{m=1}^n \\sigma(m) = \\sum_{m=1}^n m \\lfloor \\frac{n}{m} \\rfloor fails"
]

N_HYP = 0
NEG_Q_INDEX = 0