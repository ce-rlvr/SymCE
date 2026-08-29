import sympy
from sympy import Poly, reduced, lcm, expand
from sympy.abc import x, y, z, t

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "H_2: The leading monomials of f and g are relatively prime",
    "¬Q: The S-polynomial of f and g does NOT reduce to zero"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        domain_override = None
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                gens = None
                order = 'lex'
            elif len(witness) == 3:
                f, g, gens = witness
                order = 'lex'
            elif len(witness) == 4:
                f, g, gens, order = witness
            elif len(witness) == 5:
                f, g, gens, order, domain_override = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(f, Poly):
            if domain_override is None:
                domain_override = f.domain
            f = f.as_expr()
        if isinstance(g, Poly):
            if domain_override is None:
                domain_override = g.domain
            g = g.as_expr()
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False, False, False]

    try:
        if gens is None:
            free = f.free_symbols | g.free_symbols
            gens = sorted(list(free), key=lambda s: s.name)
            if not gens:
                gens = [sympy.Symbol('x')]
    except Exception:
        return [False, False, False]

    try:
        F_temp = Poly(f, *gens, order=order)
        G_temp = Poly(g, *gens, order=order)
        if domain_override is not None:
            domain = domain_override
        else:
            domain = F_temp.domain.unify(G_temp.domain)
            
        F = Poly(f, *gens, domain=domain, order=order)
        G = Poly(g, *gens, domain=domain, order=order)
        
        h1 = not F.is_zero and not G.is_zero
    except Exception:
        h1 = False

    try:
        lm_f = F.monoms()[0]
        lm_g = G.monoms()[0]
        h2 = all(min(e1, e2) == 0 for e1, e2 in zip(lm_f, lm_g))
    except Exception:
        h2 = False

    try:
        lc_f = F.coeffs()[0]
        lc_g = G.coeffs()[0]
        
        gamma_monom = tuple(max(e1, e2) for e1, e2 in zip(lm_f, lm_g))
        
        lc_f_sym = domain.to_sympy(lc_f)
        lc_g_sym = domain.to_sympy(lc_g)
        
        lc_lcm_sym = lcm(lc_f_sym, lc_g_sym)
        
        coeff_f = lc_lcm_sym / lc_f_sym
        coeff_g = lc_lcm_sym / lc_g_sym
        
        exp_f = tuple(e_g - e_f for e_g, e_f in zip(gamma_monom, lm_f))
        exp_g = tuple(e_g - e_g_orig for e_g, e_g_orig in zip(gamma_monom, lm_g))
        
        def make_term(coeff, exp, gens):
            term = coeff
            for b, e in zip(gens, exp):
                term *= b**e
            return term
            
        term_f = make_term(coeff_f, exp_f, gens)
        term_g = make_term(coeff_g, exp_g, gens)
        
        S = expand(term_f * f - term_g * g)
        
        rem1 = reduced(S, [f, g], *gens, domain=domain, order=order)[1]
        rem2 = reduced(S, [g, f], *gens, domain=domain, order=order)[1]
        
        neg_q = (not Poly(rem1, *gens).is_zero) and (not Poly(rem2, *gens).is_zero)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]