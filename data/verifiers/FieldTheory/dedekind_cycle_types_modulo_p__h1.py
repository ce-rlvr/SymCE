import sympy as sp
from sympy import Poly, factor_list
from sympy.ntheory import isprime
from sympy.abc import x, y, z

def conditions(witness):
    try:
        f_expr, p = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        if isinstance(f_expr, sp.Poly):
            f_expr = f_expr.as_expr()
        syms = list(f_expr.free_symbols)
        var = syms[0] if len(syms) == 1 else x
    except Exception:
        var = x

    try:
        f_poly = Poly(f_expr, var, domain='QQ')
        h1 = bool(f_poly.is_irreducible)
    except Exception:
        h1 = False
        f_poly = None

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        if f_poly is None:
            h3 = False
            f_mod_p = None
        else:
            coeffs = f_poly.all_coeffs()
            denoms_ok = True
            for c in coeffs:
                if hasattr(c, 'q') and c.q % p == 0:
                    denoms_ok = False
                    break
            
            if not denoms_ok:
                h3 = False
                f_mod_p = None
            else:
                f_mod_p = Poly(f_expr, var, domain=sp.GF(p))
                if f_mod_p.is_zero:
                    h3 = False
                else:
                    sqf = f_mod_p.sqf_list()
                    h3 = bool(all(mult == 1 for factor, mult in sqf[1]))
    except Exception:
        h3 = False
        f_mod_p = None

    try:
        if f_mod_p is not None and not f_mod_p.is_zero:
            factors = factor_list(f_mod_p)
            d_list = []
            for factor_poly, mult in factors[1]:
                for _ in range(mult):
                    d_list.append(factor_poly.degree())
            d_list.sort(reverse=True)
            h4 = True
        else:
            h4 = False
            d_list = []
    except Exception:
        h4 = False
        d_list = []

    try:
        if f_mod_p is not None and h1 and f_poly is not None:
            n = f_poly.degree()
            sum_d = sum(d_list)
            neg_q = bool(sum_d != n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ["H_1: f(x) is irreducible over Q", "H_2: p is a prime number", "H_3: The reduction of f(x) modulo p is square-free", "H_4: The reduction factors into irreducible polynomials of degrees d_1 to d_k", "¬Q: The Galois group does not contain an element of cycle type (d_1, ..., d_k)"]

N_HYP = 4
NEG_Q_INDEX = 4