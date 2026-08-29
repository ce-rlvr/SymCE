import sympy
from sympy import Poly, factor_list
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False, False]

    # H1: R is a Unique Factorization Domain (UFD)
    try:
        poly_a = Poly(a, x)
        poly_b = Poly(b, x)
        domain_a = poly_a.domain
        domain_b = poly_b.domain
        h1 = bool((domain_a.is_ZZ or domain_a.is_QQ) and (domain_b.is_ZZ or domain_b.is_QQ))
    except Exception:
        h1 = False

    # H2: a(x) and b(x) are polynomials in R[x]
    try:
        syms_a = a.free_symbols if hasattr(a, 'free_symbols') else set()
        syms_b = b.free_symbols if hasattr(b, 'free_symbols') else set()
        h2 = bool(syms_a.issubset({x}) and syms_b.issubset({x}))
        Poly(a, x)
        Poly(b, x)
    except Exception:
        h2 = False

    # H3: a(x) is not the zero polynomial
    try:
        h3 = not bool(Poly(a, x).is_zero)
    except Exception:
        h3 = False

    # neg_Q: a(x)y + b(x) is reducible in R[x,y]
    try:
        expr = a * y + b
        poly_a = Poly(a, x)
        poly_b = Poly(b, x)
        
        if poly_a.domain.is_ZZ and poly_b.domain.is_ZZ:
            domain = 'ZZ'
        else:
            domain = 'QQ'
        
        f_list = factor_list(expr, domain=domain)
        content = f_list[0]
        
        if domain == 'ZZ':
            content_is_unit = (abs(content) == 1)
        else:
            content_is_unit = (content != 0)
            
        num_factors = sum(power for base, power in f_list[1])
        if not content_is_unit:
            num_factors += 1
            
        neg_q = bool(num_factors >= 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: a and b are polynomials",
    "H_3: a is not the zero polynomial",
    "not Q: a y plus b is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3