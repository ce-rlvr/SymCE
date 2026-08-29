import sympy as sp
from sympy import Poly, expand, simplify, Dummy, minpoly
from sympy.abc import x, y, z, t, u, v, w
import functools

# Standard algebra objects
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

def get_content(coeffs):
    if not coeffs:
        return sp.S.Zero
    c = coeffs[0]
    for coeff in coeffs[1:]:
        c = sp.gcd(c, coeff)
    return c

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, var = witness
            elif len(witness) == 2:
                f, g = witness
                symbols = f.free_symbols | g.free_symbols
                if len(symbols) == 1:
                    var = list(symbols)[0]
                elif len(symbols) > 1:
                    var = sorted(list(symbols), key=lambda s: s.name)[0]
                else:
                    var = sp.Symbol('x')
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: f is a non-zero polynomial
    try:
        poly_f = Poly(f, var)
        h1 = not poly_f.is_zero
    except Exception:
        h1 = False
        
    # H2: g is a non-zero polynomial
    try:
        poly_g = Poly(g, var)
        h2 = not poly_g.is_zero
    except Exception:
        h2 = False
        
    # neg_Q: The content c(fg) is NOT associated to the product c(f)c(g) in R
    try:
        cf = get_content(poly_f.coeffs())
        cg = get_content(poly_g.coeffs())
        
        fg = expand(f * g)
        poly_fg = Poly(fg, var)
        cfg = get_content(poly_fg.coeffs())
        
        if cf == 0 or cg == 0:
            neg_q = False
        else:
            ratio = simplify(cfg / (cf * cg))
            
            is_unit = False
            if ratio == 1 or ratio == -1:
                is_unit = True
            elif not ratio.free_symbols:
                try:
                    Z_dummy = Dummy('Z')
                    mp = minpoly(ratio, Z_dummy)
                    coeffs = mp.all_coeffs()
                    if all(c.is_integer for c in coeffs):
                        if coeffs[0] in [1, -1] and coeffs[-1] in [1, -1]:
                            is_unit = True
                except Exception:
                    pass
            
            neg_q = not is_unit
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "H_2: g is a non-zero polynomial",
    "¬Q: The content c(fg) is not associated to the product c(f)c(g) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2