import sympy
from sympy import Poly, simplify, gcd, S

x, y, z = sympy.symbols('x y z')

def conditions(witness):
    if isinstance(witness, dict):
        f = witness.get('f')
        g = witness.get('g')
        var_x = witness.get('x', x)
        c_f = witness.get('c_f')
        c_g = witness.get('c_g')
        f_1 = witness.get('f_1')
        g_1 = witness.get('g_1')
    elif isinstance(witness, (tuple, list)):
        f = witness[0] if len(witness) > 0 else None
        g = witness[1] if len(witness) > 1 else None
        c_f = witness[2] if len(witness) > 2 else None
        c_g = witness[3] if len(witness) > 3 else None
        f_1 = witness[4] if len(witness) > 4 else None
        g_1 = witness[5] if len(witness) > 5 else None
        var_x = witness[6] if len(witness) > 6 else x
    else:
        return [False, False, False, False]

    try:
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        var_x = sympy.sympify(var_x)
        
        if c_f is None or f_1 is None:
            c_f_poly, f_1_poly = Poly(f, var_x).primitive()
            c_f = c_f if c_f is not None else c_f_poly
            f_1 = f_1 if f_1 is not None else f_1_poly.as_expr()
        
        if c_g is None or g_1 is None:
            c_g_poly, g_1_poly = Poly(g, var_x).primitive()
            c_g = c_g if c_g is not None else c_g_poly
            g_1 = g_1 if g_1 is not None else g_1_poly.as_expr()
            
        c_f = sympy.sympify(c_f)
        c_g = sympy.sympify(c_g)
        f_1 = sympy.sympify(f_1)
        g_1 = sympy.sympify(g_1)
    except Exception:
        return [False, False, False, False]

    # H1: R is a Unique Factorization Domain
    h1 = True

    # H2: c(f) and c(g) are the contents of f and g respectively
    try:
        real_c_f = Poly(f, var_x).content()
        real_c_g = Poly(g, var_x).content()
        h2 = (simplify(c_f - real_c_f) == 0) and (simplify(c_g - real_c_g) == 0)
    except Exception:
        h2 = False

    # H3: f_1 and g_1 are the primitive parts of f and g respectively
    try:
        real_f_1 = Poly(f, var_x).primitive()[1].as_expr()
        real_g_1 = Poly(g, var_x).primitive()[1].as_expr()
        h3 = (simplify(f_1 - real_f_1) == 0) and (simplify(g_1 - real_g_1) == 0)
    except Exception:
        h3 = False

    # neg_Q: gcd(f, g) != gcd(c(f), c(g)) * gcd(f_1, g_1)
    try:
        lhs = gcd(f, g)
        rhs = sympy.expand(gcd(c_f, c_g) * gcd(f_1, g_1))
        neg_q = (simplify(lhs - rhs) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: c(f) and c(g) are the contents of f and g respectively",
    "H_3: f_1 and g_1 are the primitive parts of f and g respectively",
    "not Q: The gcd of f and g is not equal to the gcd of their contents times the gcd of their primitive parts"
]

N_HYP = 3
NEG_Q_INDEX = 3