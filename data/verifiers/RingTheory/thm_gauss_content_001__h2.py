import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        g, h = witness
    except Exception:
        return [False, False, False]
        
    try:
        g_expr = sympy.sympify(g)
        h_expr = sympy.sympify(h)
        gens = list(g_expr.free_symbols | h_expr.free_symbols)
        gens = sorted(gens, key=lambda s: s.name)
        if not gens:
            gens = [sympy.Symbol('x')]
            
        poly_g = Poly(g_expr, *gens)
        poly_h = Poly(h_expr, *gens)
        
        domain = poly_g.domain.unify(poly_h.domain)
        poly_g = poly_g.set_domain(domain)
        poly_h = poly_h.set_domain(domain)
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(domain.is_UFD)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = True
    except Exception:
        h2_ok = False
        
    try:
        def is_unit(c, dom):
            if getattr(dom, 'is_Field', False):
                return c != 0
            if dom == ZZ:
                return abs(c) == 1
            return c == dom.one or c == -dom.one
            
        cont_g, _ = poly_g.primitive()
        cont_h, _ = poly_h.primitive()
        
        g_is_prim = is_unit(cont_g, poly_g.domain)
        h_is_prim = is_unit(cont_h, poly_h.domain)
        
        neg_q_ok = not (g_is_prim and h_is_prim)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: g and h are polynomials",
    "not Q: At least one of g and h is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2