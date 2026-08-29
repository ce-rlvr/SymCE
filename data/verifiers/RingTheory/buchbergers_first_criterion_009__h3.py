import sympy
from sympy import sympify, Poly, expand, reduced
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        f = sympify(witness[0])
        g = sympify(witness[1])
        if not isinstance(f, sympy.Expr) or not isinstance(g, sympy.Expr):
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    try:
        gens = list(f.free_symbols | g.free_symbols)
        gens = sorted(gens, key=lambda var: var.name)
        if gens:
            Pf = Poly(f, *gens)
            Pg = Poly(g, *gens)
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = (f != 0) and (g != 0)
        if gens:
            h2 = h2 and not Pf.is_zero and not Pg.is_zero
    except Exception:
        h2 = False

    try:
        if not gens:
            neg_q = False
        else:
            exp_f, c_f = Pf.terms()[0]
            exp_g, c_g = Pg.terms()[0]
            
            exp_lcm = tuple(max(ef, eg) for ef, eg in zip(exp_f, exp_g))
            
            mult_f_exp = tuple(el - ef for el, ef in zip(exp_lcm, exp_f))
            mult_g_exp = tuple(el - eg for el, eg in zip(exp_lcm, exp_g))
            
            def make_mono(exp, c):
                res = c
                for g_var, e in zip(gens, exp):
                    res *= g_var**e
                return res
            
            term_f = make_mono(mult_f_exp, 1 / sympify(c_f))
            term_g = make_mono(mult_g_exp, 1 / sympify(c_g))
            
            S = expand(term_f * f - term_g * g)
            
            rem1 = reduced(S, [f, g], *gens)[1]
            rem2 = reduced(S, [g, f], *gens)[1]
            
            neg_q = (expand(rem1) != 0) and (expand(rem2) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: k is a field", "H_2: f and g are non-zero polynomials", "neg_Q: S-polynomial does not reduce to zero"]

N_HYP = 2
NEG_Q_INDEX = 2