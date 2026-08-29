import sympy as sp
from sympy import Poly
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: The degrees of both f(x) and g(x) are greater than or equal to 1",
    "¬Q: The degree of the composition polynomial f(g(x)) is NOT exactly the product of the degrees of f(x) and g(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, f, g = witness
            elif len(witness) == 2:
                f, g = witness
                R = getattr(f, 'domain', None)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is an integral domain
    try:
        if R is None:
            h1 = False
        elif hasattr(R, 'is_Domain'):
            h1 = bool(R.is_Domain)
        elif hasattr(R, 'is_IntegralDomain'):
            h1 = bool(R.is_IntegralDomain)
        elif hasattr(R, 'is_integral_domain'):
            h1 = bool(R.is_integral_domain)
        elif isinstance(R, str) and R in ['ZZ', 'QQ', 'RR', 'CC', 'Z', 'Q', 'R', 'C']:
            h1 = True
        elif R in [sp.S.Integers, sp.S.Reals, sp.S.Rationals, sp.S.Complexes]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: The degrees of both f(x) and g(x) are greater than or equal to 1
    try:
        poly_f = f if isinstance(f, Poly) else Poly(f)
        poly_g = g if isinstance(g, Poly) else Poly(g)
        deg_f = poly_f.degree()
        deg_g = poly_g.degree()
        h2 = bool((deg_f >= 1) and (deg_g >= 1))
    except Exception:
        h2 = False
        
    # neg_Q: The degree of the composition polynomial f(g(x)) is NOT exactly the product of the degrees of f(x) and g(x)
    try:
        gen = poly_f.gens[0]
        expr_f = poly_f.as_expr()
        expr_g = poly_g.as_expr()
        
        comp_expr = expr_f.subs(gen, expr_g)
        
        # If f was provided as a Poly with a specific domain (e.g., Zmod(4)),
        # we compute the composition over that same domain to capture ring-specific behavior.
        if isinstance(f, Poly):
            comp_poly = Poly(comp_expr, gen, domain=f.domain)
        else:
            comp_poly = Poly(comp_expr, gen)
            
        deg_comp = comp_poly.degree()
        neg_q = bool(deg_comp != deg_f * deg_g)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]