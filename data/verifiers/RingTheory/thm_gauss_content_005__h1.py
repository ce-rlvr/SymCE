import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

def are_associates(a, b):
    if isinstance(a, sp.Poly) and isinstance(b, sp.Poly):
        if a == b or a == -b:
            return True
        try:
            q1, r1 = a.div(b)
            q2, r2 = b.div(a)
            if r1.is_zero and r2.is_zero:
                return True
        except Exception:
            pass
        return False
        
    try:
        a_expr = sp.sympify(a)
        b_expr = sp.sympify(b)
    except Exception:
        return False

    try:
        if a_expr == b_expr or a_expr == -b_expr:
            return True
        if sp.simplify(a_expr - b_expr) == 0 or sp.simplify(a_expr + b_expr) == 0:
            return True
    except Exception:
        pass
        
    try:
        q1, r1 = sp.div(a_expr, b_expr)
        q2, r2 = sp.div(b_expr, a_expr)
        if r1 == 0 and r2 == 0:
            return True
    except Exception:
        pass
        
    try:
        ratio = sp.cancel(a_expr / b_expr)
        if ratio.is_number and ratio != 0:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) < 2:
            return [False, False, False, False]
        f, g = witness[0], witness[1]
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = (f != 0) and (g != 0)
        if isinstance(f, sp.Poly):
            h1 = h1 and not f.is_zero
        if isinstance(g, sp.Poly):
            h1 = h1 and not g.is_zero
    except Exception:
        h1 = False
        
    try:
        if isinstance(f, sp.Poly) and isinstance(g, sp.Poly):
            poly_f = f
            poly_g = g
        else:
            f_expr = sp.sympify(f)
            g_expr = sp.sympify(g)
            gens_f = list(f_expr.free_symbols)
            gens_g = list(g_expr.free_symbols)
            gens = list(set(gens_f).union(set(gens_g)))
            if not gens:
                gens = [sp.Symbol('x')]
            gens = sorted(gens, key=lambda s: s.name)
            poly_f = sp.Poly(f_expr, *gens)
            poly_g = sp.Poly(g_expr, *gens)
            
        cf, pf = poly_f.primitive()
        cg, pg = poly_g.primitive()
        h2 = are_associates(cf, cg)
    except Exception:
        h2 = False
        
    try:
        if isinstance(f, sp.Poly) and isinstance(g, sp.Poly):
            poly_f = f
            poly_g = g
        else:
            f_expr = sp.sympify(f)
            g_expr = sp.sympify(g)
            gens_f = list(f_expr.free_symbols)
            gens_g = list(g_expr.free_symbols)
            gens = list(set(gens_f).union(set(gens_g)))
            if not gens:
                gens = [sp.Symbol('x')]
            gens = sorted(gens, key=lambda s: s.name)
            poly_f = sp.Poly(f_expr, *gens)
            poly_g = sp.Poly(g_expr, *gens)
            
        cf, pf = poly_f.primitive()
        cg, pg = poly_g.primitive()
        h3 = are_associates(pf, pg)
    except Exception:
        h3 = False
        
    try:
        neg_q = not are_associates(f, g)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "H_2: The contents of f and g are associates in R",
    "H_3: The primitive parts of f and g are associates in the polynomial ring",
    "not Q: The polynomials f and g are not associates in the polynomial ring"
]

N_HYP = 3
NEG_Q_INDEX = 3

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