import sympy
from sympy import Poly, QQ, ZZ, GF, Rational
from sympy.abc import x
from sympy.ntheory import legendre_symbol

# Top-level setup
# x, QQ, ZZ, GF, Rational are provided for witness construction.
# The witness should be a sympy.Poly object, e.g., Poly(x**3 - x, x, domain=QQ)

def is_square_in_domain(val, domain):
    if val == 0:
        return True
    
    try:
        val_expr = domain.to_sympy(val)
    except Exception:
        val_expr = val

    if domain.is_FiniteField:
        p = domain.characteristic
        # H1 ensures characteristic != 2, so p is an odd prime
        return legendre_symbol(int(val_expr) % p, p) != -1

    from sympy import sqrt, simplify
    try:
        s = sqrt(val_expr)
        try:
            domain.from_sympy(s)
            return True
        except Exception:
            pass
        
        s_simp = simplify(s)
        try:
            domain.from_sympy(s_simp)
            return True
        except Exception:
            pass
            
        return False
    except Exception:
        return False

def splitting_field_degree(poly):
    factors = poly.factor_list()[1]
    degrees = [f.degree() for f, m in factors]
    
    if all(d == 1 for d in degrees):
        return 1
    if any(d == 2 for d in degrees):
        return 2
    if any(d == 3 for d in degrees):
        disc = poly.discriminant()
        if is_square_in_domain(disc, poly.domain):
            return 3
        else:
            return 6
    return -1

def conditions(witness):
    # H1: F is a field of characteristic != 2, and f(x) is a cubic polynomial over F.
    try:
        if not isinstance(witness, Poly):
            h1 = False
        elif len(witness.gens) != 1:
            h1 = False
        else:
            domain = witness.domain
            char = domain.characteristic
            is_field = domain.is_Field
            deg = witness.degree()
            h1 = bool(is_field and char != 2 and deg == 3)
    except Exception:
        h1 = False

    # H2: The discriminant of f(x) is a perfect square in F.
    try:
        if not h1:
            h2 = False
        else:
            disc = witness.discriminant()
            h2 = bool(is_square_in_domain(disc, witness.domain))
    except Exception:
        h2 = False

    # neg_Q: The degree of the splitting field of f(x) over F is NOT exactly 3.
    try:
        if not h1:
            neg_q = False
        else:
            deg_sf = splitting_field_degree(witness)
            neg_q = bool(deg_sf != 3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic != 2 and f(x) is a cubic polynomial over F",
    "H_2: The discriminant of f(x) is a perfect square in F",
    "¬Q: The degree of the splitting field of f(x) over F is not exactly 3"
]

N_HYP = 2
NEG_Q_INDEX = 2