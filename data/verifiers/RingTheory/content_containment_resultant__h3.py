import functools
import math
from itertools import combinations_with_replacement
import sympy
from sympy import sympify, Symbol, Poly, resultant, igcd, groebner, reduced, Expr
from sympy.abc import x, y, z, a, b, c, d

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
            x_var = witness['x']
            n = witness['n']
            m = witness['m']
        else:
            f, g, x_var, n, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    try:
        f_sym = sympify(f)
        g_sym = sympify(g)
        h1 = isinstance(f_sym, Expr) and isinstance(g_sym, Expr)
    except Exception:
        h1 = False

    # H2: f and g are polynomials over R
    try:
        if not isinstance(x_var, Symbol):
            h2 = False
        else:
            Poly(f_sym, x_var)
            Poly(g_sym, x_var)
            h2 = True
    except Exception:
        h2 = False

    # H3: n >= 1 and m >= 1
    try:
        n_val = int(n)
        m_val = int(m)
        h3 = (n_val >= 1) and (m_val >= 1)
    except Exception:
        h3 = False

    # not Q: Res(f,g) not in c(f)^m c(g)^n
    try:
        res = resultant(f_sym, g_sym, x_var)
        
        coeffs_f = Poly(f_sym, x_var).coeffs()
        coeffs_g = Poly(g_sym, x_var).coeffs()
        
        if not coeffs_f:
            coeffs_f = [sympify(0)]
        if not coeffs_g:
            coeffs_g = [sympify(0)]
            
        gens_f = [math.prod(p) for p in combinations_with_replacement(coeffs_f, m_val)]
        gens_g = [math.prod(p) for p in combinations_with_replacement(coeffs_g, n_val)]
        
        gens = [cf * cg for cf in gens_f for cg in gens_g]
        gens = [sympify(g_i) for g_i in gens]
        res = sympify(res)
        
        if all(g_i.is_Integer for g_i in gens) and res.is_Integer:
            ideal_gcd = functools.reduce(igcd, [abs(int(g_i)) for g_i in gens])
            if ideal_gcd == 0:
                in_ideal = (res == 0)
            else:
                in_ideal = (int(res) % ideal_gcd == 0)
        elif all(g_i.is_Rational for g_i in gens) and res.is_Rational:
            if any(g_i != 0 for g_i in gens):
                in_ideal = True
            else:
                in_ideal = (res == 0)
        else:
            free_syms = set()
            for g_i in gens:
                free_syms.update(g_i.free_symbols)
            free_syms.update(res.free_symbols)
            free_syms = list(free_syms)
            
            if not free_syms:
                if any(g_i != 0 for g_i in gens):
                    in_ideal = True
                else:
                    in_ideal = (res == 0)
            else:
                gb = groebner(gens, *free_syms)
                rem = reduced(res, gb, *free_syms)[1]
                in_ideal = (rem == 0)
                
        neg_q = not in_ideal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f and g are polynomials over R",
    "H_3: n >= 1 and m >= 1",
    "not Q: The resultant Res(f,g) is not an element of the ideal c(f)^m c(g)^n"
]

N_HYP = 3
NEG_Q_INDEX = 3