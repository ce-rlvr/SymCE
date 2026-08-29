import sympy as sp

S3 = sp.combinatorics.SymmetricGroup(3)
S4 = sp.combinatorics.SymmetricGroup(4)
A4 = sp.combinatorics.AlternatingGroup(4)
D4 = sp.combinatorics.DihedralGroup(4)
C4 = sp.combinatorics.CyclicGroup(4)
V4 = sp.combinatorics.AlternatingGroup(4)
Z2 = sp.combinatorics.CyclicGroup(2)
Z3 = sp.combinatorics.CyclicGroup(3)
Z4 = sp.combinatorics.CyclicGroup(4)
Z6 = sp.combinatorics.CyclicGroup(6)
trivial = sp.combinatorics.CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f and g are non-zero polynomials",
    "H_3: f_1 and g_1 are the primitive parts of f and g respectively",
    "neg_Q: The greatest common divisor of f and g is not equal to gcd(c(f), c(g)) * gcd(f_1, g_1)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        f, g, f_1, g_1, x = witness
    except Exception:
        return [False, False, False, False]

    try:
        poly_f = sp.Poly(f, x)
        poly_g = sp.Poly(g, x)
        h1_ok = bool(poly_f.domain.is_UFD and poly_g.domain.is_UFD)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(f != 0 and g != 0)
    except Exception:
        h2_ok = False

    try:
        c_f, true_f_1 = poly_f.primitive()
        c_g, true_g_1 = poly_g.primitive()
        f_1_expr = f_1.as_expr() if hasattr(f_1, 'as_expr') else f_1
        g_1_expr = g_1.as_expr() if hasattr(g_1, 'as_expr') else g_1
        h3_ok = bool(sp.simplify(f_1_expr - true_f_1.as_expr()) == 0 and sp.simplify(g_1_expr - true_g_1.as_expr()) == 0)
    except Exception:
        h3_ok = False

    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
        
        gcd_fg = sp.gcd(f_expr, g_expr)
        gcd_c = sp.gcd(c_f, c_g)
        gcd_R = sp.gcd(f_1_expr, g_1_expr)
        
        rhs = sp.simplify(gcd_c * gcd_R)
        
        neg_q_ok = bool(sp.simplify(gcd_fg - rhs) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]