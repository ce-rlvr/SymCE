import sympy
from sympy import Poly

# Top-level setup: named object bindings
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g) or (R, f, g) where f and g are polynomials in x.
    """
    try:
        if len(witness) == 3:
            R, f, g = witness
            poly_f = Poly(f, x, domain=R)
            poly_g = Poly(g, x, domain=R)
            domain = poly_f.domain
        elif len(witness) == 2:
            f, g = witness
            poly_f = Poly(f, x)
            poly_g = Poly(g, x)
            domain = poly_f.domain.unify(poly_g.domain)
            poly_f = Poly(f, x, domain=domain)
            poly_g = Poly(g, x, domain=domain)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False

    # H_2: f is a primitive polynomial over R
    try:
        cont_f = poly_f.primitive()[0]
        try:
            h2 = bool(domain.is_unit(cont_f))
        except AttributeError:
            # Fallback if is_unit is not implemented for the domain
            h2 = bool(cont_f == domain.one or cont_f == -domain.one)
    except Exception:
        h2 = False

    # ¬Q: g is NOT a primitive polynomial
    try:
        cont_g = poly_g.primitive()[0]
        try:
            is_unit_g = bool(domain.is_unit(cont_g))
        except AttributeError:
            is_unit_g = bool(cont_g == domain.one or cont_g == -domain.one)
        neg_q = not is_unit_g
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: f is a primitive polynomial over R",
    "¬Q: g is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2