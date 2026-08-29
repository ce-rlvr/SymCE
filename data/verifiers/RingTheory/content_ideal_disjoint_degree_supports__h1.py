import sympy
import itertools
import functools
from sympy.abc import x, y, z
from sympy import QQ, ZZ, Rational, Integer

CONDITION_LABELS = [
    "H_1: f and g are polynomials",
    "H_2: The set of degrees of non-zero terms of f and g are disjoint",
    "not Q: The content ideal c(f+g) is NOT exactly equal to the sum of the content ideals c(f) + c(g)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, main_var = witness
            elif len(witness) == 2:
                f, g = witness
                syms = sorted(list(f.free_symbols | g.free_symbols), key=lambda s: s.name)
                main_var = syms[0] if syms else sympy.Symbol('x')
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        poly_f = sympy.Poly(f, main_var)
        poly_g = sympy.Poly(g, main_var)
        h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            deg_f = set(monom[0] for monom in poly_f.monoms() if poly_f.coeff_monomial(monom) != 0)
            deg_g = set(monom[0] for monom in poly_g.monoms() if poly_g.coeff_monomial(monom) != 0)
            h2 = deg_f.isdisjoint(deg_g)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            poly_fg = sympy.Poly(f + g, main_var)
            
            coeffs_f = poly_f.coeffs()
            coeffs_g = poly_g.coeffs()
            coeffs_fg = poly_fg.coeffs()
            
            base_vars = list((f.free_symbols | g.free_symbols) - {main_var})
            
            is_QQ = False
            for poly in (poly_f, poly_g):
                for coeff in poly.coeffs():
                    if coeff.is_Rational and not coeff.is_Integer:
                        is_QQ = True
                        break
            
            ideals_equal = True
            if is_QQ:
                try:
                    if not base_vars:
                        c_f = functools.reduce(sympy.gcd, coeffs_f, sympy.S.Zero)
                        c_g = functools.reduce(sympy.gcd, coeffs_g, sympy.S.Zero)
                        c_fg = functools.reduce(sympy.gcd, coeffs_fg, sympy.S.Zero)
                        ideals_equal = ((c_fg == 0) == (c_f == 0 and c_g == 0))
                    else:
                        c_f = functools.reduce(sympy.gcd, coeffs_f, sympy.S.Zero)
                        c_g = functools.reduce(sympy.gcd, coeffs_g, sympy.S.Zero)
                        c_fg = functools.reduce(sympy.gcd, coeffs_fg, sympy.S.Zero)
                        gb1 = sympy.groebner([c_fg], *base_vars, domain='QQ')
                        gb2 = sympy.groebner([c_f, c_g], *base_vars, domain='QQ')
                        ideals_equal = (list(gb1) == list(gb2))
                except Exception:
                    pass
            else:
                if not base_vars:
                    c_f = functools.reduce(sympy.gcd, coeffs_f, sympy.S.Zero)
                    c_g = functools.reduce(sympy.gcd, coeffs_g, sympy.S.Zero)
                    c_fg = functools.reduce(sympy.gcd, coeffs_fg, sympy.S.Zero)
                    ideals_equal = (abs(c_fg) == abs(sympy.gcd(c_f, c_g)))
                else:
                    c_f = functools.reduce(sympy.gcd, coeffs_f, sympy.S.Zero)
                    c_g = functools.reduce(sympy.gcd, coeffs_g, sympy.S.Zero)
                    c_fg = functools.reduce(sympy.gcd, coeffs_fg, sympy.S.Zero)
                    for vals in itertools.product(range(-3, 4), repeat=len(base_vars)):
                        subs = dict(zip(base_vars, vals))
                        try:
                            val_f = c_f.subs(subs)
                            val_g = c_g.subs(subs)
                            val_fg = c_fg.subs(subs)
                            
                            if not (val_f.is_Integer and val_g.is_Integer and val_fg.is_Integer):
                                continue
                                
                            if abs(val_fg) != abs(sympy.gcd(val_f, val_g)):
                                ideals_equal = False
                                break
                        except Exception:
                            pass
            
            neg_q = not ideals_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]