import sympy
from sympy import symbols, Poly, Rational, Integer, QQ, ZZ, GF
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "If k is a field and the leading monomials of f and g are relatively prime,
    then the S-polynomial of f and g reduces to zero modulo {f, g}."
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            gens = witness.get('gens', None)
            domain = witness.get('domain', None)
            order = witness.get('order', 'lex')
        elif isinstance(witness, (list, tuple)):
            f = witness[0]
            g = witness[1]
            gens = witness[2] if len(witness) > 2 else None
            domain = witness[3] if len(witness) > 3 else None
            order = witness[4] if len(witness) > 4 else 'lex'
        else:
            return [False, False, False]
            
        if isinstance(f, sympy.Poly):
            f = f.as_expr()
        if isinstance(g, sympy.Poly):
            g = g.as_expr()
            
        if gens is None:
            gens = list(f.free_symbols | g.free_symbols)
            gens.sort(key=lambda s: s.name)
            if not gens:
                gens = [sympy.Symbol('x')]
                
        kwargs = {'order': order}
        if domain is not None:
            kwargs['domain'] = domain
            
        poly_f = sympy.Poly(f, *gens, **kwargs)
        poly_g = sympy.Poly(g, *gens, **kwargs)
    except Exception:
        return [False, False, False]

    # H_1: k is a field
    try:
        h1 = bool(poly_f.domain.is_Field and poly_g.domain.is_Field)
    except Exception:
        h1 = False

    # H_2: The leading monomials of f and g with respect to a given monomial order are relatively prime
    try:
        lm_f = poly_f.LM()
        lm_g = poly_g.LM()
        h2 = all(min(a, b) == 0 for a, b in zip(lm_f, lm_g))
    except Exception:
        h2 = False

    # neg_Q: The S-polynomial of f and g does NOT reduce to zero modulo {f, g}
    try:
        gamma = tuple(max(a, b) for a, b in zip(lm_f, lm_g))
        
        def make_term(coef, exp_tuple, gens):
            term = coef
            for g_var, exp in zip(gens, exp_tuple):
                term *= g_var**exp
            return term
            
        term_f = make_term(sympy.S(1) / poly_f.LC(), tuple(g_exp - f_exp for g_exp, f_exp in zip(gamma, lm_f)), gens)
        term_g = make_term(sympy.S(1) / poly_g.LC(), tuple(g_exp - g_exp_ for g_exp, g_exp_ in zip(gamma, lm_g)), gens)
        
        s_poly_expr = sympy.expand(term_f * f - term_g * g)
        
        def custom_reduced(expr, divisors, gens, kwargs, max_steps=1000):
            p = sympy.Poly(expr, *gens, **kwargs)
            divs = [sympy.Poly(d, *gens, **kwargs) for d in divisors]
            
            rem = sympy.Poly(0, *gens, **kwargs)
            
            steps = 0
            while not p.is_zero and steps < max_steps:
                steps += 1
                lm_p = p.LM()
                lc_p = p.LC()
                
                divided = False
                for d in divs:
                    if d.is_zero:
                        continue
                    lm_d = d.LM()
                    if all(a >= b for a, b in zip(lm_p, lm_d)):
                        exp_diff = tuple(a - b for a, b in zip(lm_p, lm_d))
                        coef = sympy.S(lc_p) / d.LC()
                        term_poly = sympy.Poly.from_dict({exp_diff: coef}, *gens, **kwargs)
                        p = p - term_poly * d
                        divided = True
                        break
                        
                if not divided:
                    lt_poly = sympy.Poly.from_dict({lm_p: lc_p}, *gens, **kwargs)
                    rem = rem + lt_poly
                    p = p - lt_poly
                    
            return rem, steps >= max_steps

        rem1, timeout1 = custom_reduced(s_poly_expr, [f, g], gens, kwargs)
        rem2, timeout2 = custom_reduced(s_poly_expr, [g, f], gens, kwargs)
        
        reduces_to_zero = (rem1.is_zero and not timeout1) or (rem2.is_zero and not timeout2)
        
        neg_q = not reduces_to_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: The leading monomials of f and g with respect to a given monomial order are relatively prime",
    "¬Q: The S-polynomial of f and g does NOT reduce to zero modulo {f, g}"
]

N_HYP = 2
NEG_Q_INDEX = 2