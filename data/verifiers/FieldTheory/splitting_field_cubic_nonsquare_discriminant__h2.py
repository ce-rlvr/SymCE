import sympy as sp
from sympy import Poly, Symbol

# Top-level setup for witness expressions
x = Symbol('x')
y = Symbol('y')

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2 and f is a cubic polynomial",
    "H_2: The discriminant of f(x) is not a perfect square in F",
    "¬Q: The degree of the splitting field of f(x) over F is not exactly 6"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, sp.Poly):
            f = witness
        else:
            free_syms = witness.free_symbols
            if len(free_syms) == 1:
                var = list(free_syms)[0]
                f = sp.Poly(witness, var)
            else:
                f = sp.Poly(witness, x)
    except Exception:
        return [False, False, False]
    
    try:
        domain = f.domain
        if not domain.is_Field:
            domain = domain.get_field()
            f = f.set_domain(domain)
        
        char = domain.characteristic
        h1 = (f.degree() == 3) and (char != 2)
    except Exception:
        h1 = False

    try:
        var = f.gen
        expr = f.as_expr()
        Delta = sp.discriminant(expr, var)
        
        # Check if Delta is a perfect square in the field F
        sq_poly = sp.Poly(y**2 - Delta, y, domain=domain)
        is_sq = not sq_poly.is_irreducible
        h2 = not is_sq
    except Exception:
        h2 = False

    try:
        # For a cubic polynomial over a field of char != 2, the splitting field 
        # has degree exactly 6 if and only if it is irreducible and its discriminant 
        # is not a perfect square in the base field.
        is_deg_6 = f.is_irreducible and (not is_sq)
        neg_q = not is_deg_6
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]