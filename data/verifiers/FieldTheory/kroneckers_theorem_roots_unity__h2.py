import sympy
from sympy import Dummy, Poly, minpoly

# Top-level setup
# No specific named bindings required for this domain

def conditions(witness) -> list[bool]:
    # H_1: alpha is a non-zero algebraic integer
    try:
        if witness == 0:
            h1_ok = False
        else:
            x = Dummy('x')
            p = minpoly(witness, x)
            poly = Poly(p, x)
            h1_ok = all(c.is_integer for c in poly.coeffs())
    except Exception:
        h1_ok = False

    # neg_Q: alpha is not a root of unity
    try:
        x = Dummy('x')
        p = minpoly(witness, x)
        poly = Poly(p, x)
        
        is_alg_int = all(c.is_integer for c in poly.coeffs())
        if not is_alg_int:
            # If it's not an algebraic integer, it cannot be a root of unity
            is_root_of_unity = False
        else:
            roots = poly.nroots()
            is_root_of_unity = True
            for r in roots:
                modulus = abs(r).evalf()
                if float(abs(modulus - 1)) > 1e-7:
                    is_root_of_unity = False
                    break
                    
        neg_q_ok = not is_root_of_unity
    except Exception:
        # If minpoly fails, it's not an algebraic number, hence not a root of unity
        if isinstance(witness, sympy.Expr):
            neg_q_ok = True
        else:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is a non-zero algebraic integer",
    "¬Q: alpha is not a root of unity"
]

N_HYP = 1
NEG_Q_INDEX = 1