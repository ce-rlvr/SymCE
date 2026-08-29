import sympy
from sympy import Symbol, sympify

# Top-level setup
x = Symbol('x')

def is_zero(expr):
    """Safely check if a SymPy expression is mathematically zero."""
    try:
        expr = sympify(expr)
        if expr == 0:
            return True
        if hasattr(expr, 'equals'):
            eq = expr.equals(0)
            if eq is True:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness tuple (n, zeta), checks if it is a counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        n, zeta = witness
    except Exception:
        return [False, False]
        
    # H_1: zeta is a complex root of the n-th cyclotomic polynomial Phi_n(x)
    try:
        if not isinstance(n, (int, sympy.Integer)) or n < 1:
            h1 = False
        else:
            poly = sympy.cyclotomic_poly(n, x)
            val = poly.subs(x, zeta)
            h1 = is_zero(val)
    except Exception:
        h1 = False
        
    # neg_Q: zeta^{-1} is NOT a root of Phi_n(x), OR zeta^{-1} == zeta
    try:
        if not isinstance(n, (int, sympy.Integer)) or n < 1:
            neg_q = False
        else:
            poly = sympy.cyclotomic_poly(n, x)
            zeta_inv = 1 / sympify(zeta)
            val_inv = poly.subs(x, zeta_inv)
            
            is_root = is_zero(val_inv)
            is_eq = is_zero(zeta_inv - zeta)
            
            neg_q = (not is_root) or is_eq
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: zeta is a complex root of the n-th cyclotomic polynomial Phi_n(x)",
    "¬Q: zeta^{-1} is not a root of Phi_n(x) or zeta^{-1} == zeta"
]

N_HYP = 1
NEG_Q_INDEX = 1