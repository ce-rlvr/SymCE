import sympy
from sympy import abc

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for Capelli's Lemma on Polynomial Composition.
    The dropped hypothesis is that f(x) is irreducible over K.
    Witness is expected to be a tuple (f, g) or (K, f, g).
    """
    try:
        if len(witness) == 3:
            K, f, g = witness
            K_is_field = getattr(K, 'is_Field', True)
        elif len(witness) == 2:
            f, g = witness
            K_is_field = True
        else:
            return [False, False, False, False]
        
        if isinstance(f, sympy.Poly):
            f = f.as_expr()
        else:
            f = sympy.sympify(f)
            
        if isinstance(g, sympy.Poly):
            g = g.as_expr()
        else:
            g = sympy.sympify(g)
            
    except Exception:
        return [False, False, False, False]

    # H1: K is a field
    h1 = bool(K_is_field)

    # H2: f and g are polynomials over K
    try:
        pf = sympy.Poly(f, x, domain='QQ')
        pg = sympy.Poly(g, x, domain='QQ')
        h2 = True
    except Exception:
        h2 = False

    # H3: There exists a root alpha of f(x) in its splitting field such that g(x) - alpha is irreducible over K(alpha)
    h3 = False
    try:
        if h2:
            roots = sympy.solve(f, x)
            for r in roots:
                try:
                    if r.is_Rational:
                        factors = sympy.factor_list(g - r, domain='QQ')
                    else:
                        factors = sympy.factor_list(g - r, extension=r)
                    
                    # Irreducible if there is exactly one polynomial factor with multiplicity 1
                    if len(factors[1]) == 1 and factors[1][0][1] == 1:
                        h3 = True
                        break
                except Exception:
                    continue
    except Exception:
        pass

    # neg_Q: f(g(x)) is reducible over K
    neg_q = False
    try:
        if h2:
            fg = f.subs(x, g)
            factors = sympy.factor_list(fg, domain='QQ')
            is_irred = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            neg_q = not is_irred
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f and g are polynomials over K",
    "H_3: There exists a root alpha of f in its splitting field such that g - alpha is irreducible over K(alpha)",
    "¬Q: f(g) is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3