import sympy
from sympy import QQ, ZZ, Symbol, Expr, gcd, lcm
from sympy.polys.polytools import reduced, groebner

x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        gens, ring_vars, domain = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is an integral domain
    try:
        if domain in (QQ, 'QQ'):
            dom_obj = QQ
        elif domain in (ZZ, 'ZZ'):
            dom_obj = ZZ
        else:
            dom_obj = None
            
        h1 = (dom_obj is not None) and isinstance(ring_vars, (list, tuple)) and len(ring_vars) > 0 and all(isinstance(v, Symbol) for v in ring_vars)
    except Exception:
        h1 = False
        
    # H2: M is a non-zero fractional ideal of R in K
    try:
        if not isinstance(gens, (list, tuple)) or len(gens) == 0:
            h2 = False
        else:
            h2 = False
            has_nonzero = False
            valid = True
            for g in gens:
                if not isinstance(g, Expr) and not isinstance(g, (int, float)):
                    valid = False
                    break
                g_expr = sympy.cancel(sympy.sympify(g))
                if not g_expr.free_symbols.issubset(set(ring_vars)):
                    valid = False
                    break
                num, den = g_expr.as_numer_denom()
                if not num.is_polynomial(*ring_vars) or not den.is_polynomial(*ring_vars):
                    valid = False
                    break
                if sympy.expand(num) != 0:
                    has_nonzero = True
            if valid and has_nonzero:
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: M is not a principal fractional ideal
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            gens_expr = [sympy.sympify(g) for g in gens]
            fracs = [sympy.cancel(g).as_numer_denom() for g in gens_expr]
            
            # Compute LCM of denominators
            den_lcm = sympy.S.One
            for _, den in fracs:
                den_lcm = lcm(den_lcm, den)
            
            polys = []
            for num, den in fracs:
                multiplier = sympy.cancel(den_lcm / den)
                polys.append(sympy.expand(num * multiplier))
            
            # Compute GCD of polys
            d = polys[0]
            for p in polys[1:]:
                d = gcd(d, p)
            
            # Compute Groebner basis
            G = groebner(polys, *ring_vars, domain=dom_obj)
            
            # Reduce d modulo G
            _, rem = reduced(d, list(G), *ring_vars, domain=dom_obj)
            
            is_principal = (sympy.expand(rem) == 0)
            neg_q = not is_principal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain and K is its field of fractions",
    "H_2: M is a non-zero fractional ideal of R in K",
    "¬Q: M is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2