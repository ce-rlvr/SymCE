import sympy
from sympy import Poly, Symbol
from sympy.abc import x
from sympy.ntheory import factorint

# Top-level setup
x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            d = witness.get('d')
            I = witness.get('I')
        else:
            d, I = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: d is a square-free integer
    try:
        d_val = int(d)
        if d_val != d:
            h1 = False
        elif d_val == 0:
            h1 = False
        else:
            factors = factorint(abs(d_val))
            h1 = all(exp == 1 for exp in factors.values())
    except Exception:
        h1 = False
        
    # H2: d = 2 mod 4 or d = 3 mod 4
    try:
        h2 = (d_val % 4 == 2) or (d_val % 4 == 3)
    except Exception:
        h2 = False
        
    # H3: I is a polynomial or list of polynomials in Z_x
    try:
        if not isinstance(I, (list, tuple, set)):
            I_list = [I]
        else:
            I_list = list(I)
            
        symbols = set()
        for p in I_list:
            if hasattr(p, 'free_symbols'):
                symbols.update(p.free_symbols)
        
        if len(symbols) == 1:
            x_sym = list(symbols)[0]
        elif len(symbols) == 0:
            x_sym = x
        else:
            x_sym = None
            
        if x_sym is not None:
            h3 = True
            polys = []
            for p in I_list:
                poly = Poly(p, x_sym)
                if not all(c.is_integer for c in poly.coeffs()):
                    h3 = False
                    break
                polys.append(poly.set_domain('ZZ'))
            if len(polys) == 0:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: R mod I is NOT isomorphic to Z_sqrt_d
    try:
        if not h3:
            neg_q = False
        else:
            is_iso = False
            g = polys[0]
            for p in polys[1:]:
                g = g.gcd(p)
                
            if g.degree() == 2:
                lc = g.LC()
                if lc in (1, -1):
                    g = g * lc
                    coeffs = g.all_coeffs()
                    b = coeffs[1]
                    c = coeffs[2]
                    if b % 2 == 0:
                        a = -b // 2
                        if c == a**2 - d_val:
                            if len(polys) == 1:
                                is_iso = True
                            else:
                                try:
                                    from sympy import groebner
                                    quotients = [p.exquo(g) for p in polys]
                                    gb = groebner(quotients, x_sym, domain='ZZ')
                                    if len(gb) == 1 and gb[0] in (1, -1):
                                        is_iso = True
                                except Exception:
                                    # Fallback to True to avoid false positives on tricky valid ideals
                                    is_iso = True
            neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: d is a square-free integer",
    "H_2: d is 2 or 3 mod 4",
    "H_3: I is an ideal in Z_x",
    "neg_Q: R mod I is not isomorphic to the ring of algebraic integers of Q_sqrt_d"
]

N_HYP = 3
NEG_Q_INDEX = 3