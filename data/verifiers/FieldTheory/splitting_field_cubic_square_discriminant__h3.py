import sympy
from sympy import Poly, Symbol, QQ, ZZ, GF, Rational
from sympy.abc import x, y, z, t

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f(x) is an irreducible polynomial of degree 3 over F",
    "¬Q: The degree of the splitting field of f(x) over F is not 3"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, Poly):
            witness = Poly(witness)
    except Exception:
        pass

    # H_1: F is a field of characteristic not equal to 2
    try:
        domain = witness.domain
        h1 = bool(domain.is_Field and domain.characteristic != 2)
    except Exception:
        h1 = False

    # H_2: f(x) is an irreducible polynomial of degree 3 over F
    try:
        h2 = bool(getattr(witness, 'is_univariate', False) and 
                  witness.degree() == 3 and 
                  witness.is_irreducible)
    except Exception:
        h2 = False

    # ¬Q: The degree of the splitting field of f(x) over F is not 3
    try:
        if not getattr(witness, 'is_univariate', False):
            neg_q = False
        elif witness.degree() != 3:
            neg_q = True
        else:
            if witness.is_irreducible:
                d = witness.discriminant()
                domain = witness.domain
                d_expr = domain.to_sympy(d)
                x_sym = witness.gens[0]
                
                # For an irreducible cubic over a field, the splitting field has degree 3 
                # if and only if the discriminant is a square in the base field.
                # Otherwise, the degree is 6.
                test_poly = Poly(x_sym**2 - d_expr, x_sym, domain=domain)
                is_square = not test_poly.is_irreducible
                deg_sf = 3 if is_square else 6
            else:
                # If it is reducible, the splitting field degree is 1 or 2 (not 3).
                deg_sf = 1
                
            neg_q = bool(deg_sf != 3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]