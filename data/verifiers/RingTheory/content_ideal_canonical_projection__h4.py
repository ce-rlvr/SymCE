import sympy as sp
from sympy import Poly, Symbol, Expr
from sympy.abc import x, y, z, t, u, v
import functools

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False, False]
        f, poly_x, I_gens = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        f = sp.sympify(f)
        h1 = isinstance(f, Expr) and isinstance(poly_x, Symbol)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(I_gens, list) and all(isinstance(sp.sympify(g), Expr) for g in I_gens)
    except Exception:
        h2 = False
        
    h3 = h1 and h2
    
    try:
        f_poly = Poly(f, poly_x)
        coeffs = f_poly.all_coeffs()
        
        if not coeffs:
            c_f = sp.S.Zero
        else:
            c_f = functools.reduce(sp.gcd, coeffs)
        
        ring_vars = set()
        for c in coeffs:
            ring_vars.update(c.free_symbols)
        for g in I_gens:
            ring_vars.update(sp.sympify(g).free_symbols)
        ring_vars.discard(poly_x)
        ring_vars = sorted(list(ring_vars), key=lambda s: s.name)
        
        if not ring_vars:
            ideal1_zero = all(sp.simplify(sp.sympify(c)) == 0 for c in coeffs + I_gens)
            ideal2_zero = all(sp.simplify(sp.sympify(c)) == 0 for c in [c_f] + I_gens)
            ideals_equal = (ideal1_zero == ideal2_zero)
        else:
            gb1 = sp.groebner(coeffs + I_gens, *ring_vars, domain='QQ')
            gb2 = sp.groebner([c_f] + I_gens, *ring_vars, domain='QQ')
            ideals_equal = set(gb1) == set(gb2)
            
        neg_q = not ideals_equal
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "H_3: pi: R -> R/I is the canonical projection homomorphism",
    "¬Q: The content ideal of the projected polynomial pi(f) over R/I is NOT equal to (c(f) + I) / I"
]

N_HYP = 3
NEG_Q_INDEX = 3