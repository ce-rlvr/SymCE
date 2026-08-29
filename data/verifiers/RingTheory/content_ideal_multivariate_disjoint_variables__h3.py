import sympy as sp
import math
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, t, u, v, a, b, c, d = sp.symbols('x y t u v a b c d')

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
        f = sp.sympify(f)
        g = sp.sympify(g)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    h1_ok = True
    
    # H_2: f is a polynomial in x over R
    try:
        if y in f.free_symbols:
            h2_ok = False
        else:
            sp.Poly(f, x)
            h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: The content ideal of fg is NOT equal to c(f)c(g)
    try:
        fg = sp.expand(f * g)
        
        base_vars = list((f.free_symbols | g.free_symbols) - {x, y})
        
        poly_f = sp.Poly(f, x, y)
        poly_g = sp.Poly(g, x, y)
        poly_fg = sp.Poly(fg, x, y)
        
        coeffs_f = poly_f.coeffs()
        coeffs_g = poly_g.coeffs()
        coeffs_fg = poly_fg.coeffs()
        
        gens_cfg = [a_c * b_c for a_c in coeffs_f for b_c in coeffs_g]
        gens_fg = coeffs_fg
        
        if not base_vars:
            try:
                for coeff in gens_cfg + gens_fg:
                    if not coeff.is_integer:
                        raise TypeError
                gcd1 = functools.reduce(math.gcd, [int(coeff) for coeff in gens_cfg], 0)
                gcd2 = functools.reduce(math.gcd, [int(coeff) for coeff in gens_fg], 0)
                ideals_eq = (abs(gcd1) == abs(gcd2))
            except (TypeError, AttributeError):
                is_zero1 = all(sp.simplify(coeff) == 0 for coeff in gens_cfg)
                is_zero2 = all(sp.simplify(coeff) == 0 for coeff in gens_fg)
                ideals_eq = (is_zero1 == is_zero2)
        else:
            try:
                gb1 = list(sp.groebner(gens_cfg, *base_vars, domain='ZZ'))
                gb2 = list(sp.groebner(gens_fg, *base_vars, domain='ZZ'))
                domain = 'ZZ'
            except Exception:
                gb1 = list(sp.groebner(gens_cfg, *base_vars))
                gb2 = list(sp.groebner(gens_fg, *base_vars))
                domain = None
                
            ideals_eq = True
            for gen in gens_cfg:
                kwargs = {'domain': domain} if domain else {}
                if sp.reduced(gen, gb2, *base_vars, **kwargs)[1] != 0:
                    ideals_eq = False
                    break
            if ideals_eq:
                for gen in gens_fg:
                    kwargs = {'domain': domain} if domain else {}
                    if sp.reduced(gen, gb1, *base_vars, **kwargs)[1] != 0:
                        ideals_eq = False
                        break
                        
        neg_q_ok = not ideals_eq
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial in x over R",
    "¬Q: The content ideal of fg is NOT equal to c(f)c(g)"
]

N_HYP = 2
NEG_Q_INDEX = 2