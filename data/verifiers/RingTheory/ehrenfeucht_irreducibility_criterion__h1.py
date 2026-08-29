import sympy
import math

# Top-level setup
x, y = sympy.symbols('x y')

def conditions(witness):
    try:
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False] * 6

    # H1: f(x) in K[x]
    try:
        h1 = bool(f.is_polynomial(x) and f.free_symbols.issubset({x}))
    except Exception:
        h1 = False

    # H2: g(y) in K[y]
    try:
        h2 = bool(g.is_polynomial(y) and g.free_symbols.issubset({y}))
    except Exception:
        h2 = False

    # H3: deg(f) >= 1
    try:
        deg_f = sympy.degree(f, x)
        h3 = bool(deg_f >= 1)
    except Exception:
        h3 = False

    # H4: deg(g) >= 1
    try:
        deg_g = sympy.degree(g, y)
        h4 = bool(deg_g >= 1)
    except Exception:
        h4 = False

    # H5: gcd(deg(f), deg(g)) == 1
    try:
        h5 = bool(math.gcd(int(deg_f), int(deg_g)) == 1)
    except Exception:
        h5 = False

    # ¬Q: f(x) - g(y) is reducible in K[x,y]
    try:
        poly_fg = f - g
        _, factors = sympy.factor_list(poly_fg)
        
        non_units = sum(mult for fac, mult in factors if not fac.is_number)
        neg_q = bool(non_units > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial in x",
    "H_2: g is a polynomial in y",
    "H_3: deg f >= 1",
    "H_4: deg g >= 1",
    "H_5: gcd of deg f and deg g is 1",
    "¬Q: f - g is reducible"
]

N_HYP = 5
NEG_Q_INDEX = 5