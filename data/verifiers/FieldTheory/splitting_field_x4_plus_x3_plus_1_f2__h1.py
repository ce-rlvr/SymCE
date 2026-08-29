import math
from sympy import Poly, Symbol
from sympy.ntheory import factorint

x = Symbol('x')

def get_field_info(E):
    if hasattr(E, 'order') and hasattr(E, 'characteristic'):
        try:
            char = int(E.characteristic)
            order = int(E.order)
            if char > 1 and order >= char:
                degree = int(round(math.log(order, char)))
                return char, degree, order
        except Exception:
            pass
            
    if isinstance(E, int) and E > 1:
        try:
            factors = factorint(E)
            if len(factors) == 1:
                char = list(factors.keys())[0]
                degree = factors[char]
                return char, degree, E
        except Exception:
            pass
            
    return None, None, None

def get_splitting_field_order(f_poly):
    factors = f_poly.factor_list()
    lcm_deg = 1
    for factor, mult in factors[1]:
        deg = factor.degree()
        lcm_deg = (lcm_deg * deg) // math.gcd(lcm_deg, deg)
    return 2**lcm_deg

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        f, E = witness
    else:
        f = x**4 + x**3 + 1
        E = witness

    h1 = False
    try:
        f_poly = Poly(f, x, domain='GF(2)')
        expected = Poly(x**4 + x**3 + 1, x, domain='GF(2)')
        h1 = (f_poly == expected)
    except Exception:
        h1 = False

    h2 = False
    try:
        char, degree, order = get_field_info(E)
        if char == 2:
            f_poly = Poly(f, x, domain='GF(2)')
            expected_order = get_splitting_field_order(f_poly)
            if order == expected_order:
                h2 = True
    except Exception:
        h2 = False

    neg_q = False
    try:
        char, degree, order = get_field_info(E)
        if char == 2:
            is_deg_4 = (degree == 4)
            is_F16 = (order == 16)
            neg_q = not (is_deg_4 and is_F16)
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^4 + x^3 + 1 in F_2 polynomials",
    "H_2: E is the splitting field of f(x) over F_2",
    "¬Q: The degree of the extension E over F_2 is not 4, or E is not isomorphic to F_16"
]

N_HYP = 2
NEG_Q_INDEX = 2