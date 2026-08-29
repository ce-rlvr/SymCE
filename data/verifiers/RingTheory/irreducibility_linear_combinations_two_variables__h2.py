import sympy as sp
from sympy import degree, gcd, factor_list
from sympy.abc import x, y

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

def conditions(witness):
    try:
        if len(witness) == 3:
            domain, f, g = witness
        elif len(witness) == 2:
            f, g = witness
            domain = sp.QQ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False

    try:
        if not f.free_symbols.issubset({x}) or not g.free_symbols.issubset({x}):
            h2 = False
        elif not f.is_polynomial(x) or not g.is_polynomial(x):
            h2 = False
        else:
            d = gcd(f, g, domain=domain)
            h2 = bool(degree(d, x) == 0)
    except Exception:
        h2 = False

    try:
        if not f.is_polynomial(x) or not g.is_polynomial(x):
            h3 = False
        else:
            deg_f = degree(f, x)
            deg_g = degree(g, x)
            
            if deg_f == sp.oo or deg_f == -sp.oo:
                deg_f = -1
            if deg_g == sp.oo or deg_g == -sp.oo:
                deg_g = -1
                
            h3 = bool(max(deg_f, deg_g) >= 1)
    except Exception:
        h3 = False

    try:
        poly_xy = f + y * g
        coeff, factors = factor_list(poly_xy, domain=domain)
        num_factors = sum(mult for fac, mult in factors)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: gcd of f and g is 1",
    "H_3: max degree of f and g is at least 1",
    "not Q: f + y*g is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3