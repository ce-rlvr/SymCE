import sympy as sp
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be:
      - A dictionary with keys 'g', 'h', 'f'
      - A tuple (g, h, f) or (g, h)
      - A single sympy expression f(x,y), from which g(x) (leading coefficient in y) 
        and h(x) (constant term in y) are inferred.
    """
    try:
        if isinstance(witness, dict):
            g = witness.get('g')
            h = witness.get('h')
            f = witness.get('f')
            
            if f is not None:
                f = sp.sympify(f)
                if g is None or h is None:
                    syms = list(f.free_symbols)
                    main_var = y if y in syms else (x if x in syms else y)
                    f_poly = sp.Poly(f, main_var)
                    if g is None: g = f_poly.LC()
                    if h is None: h = f.subs(main_var, 0)
            else:
                if g is not None and h is not None:
                    g = sp.sympify(g)
                    h = sp.sympify(h)
                    f = g * y + h
                else:
                    return [False, False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                g, h, f = witness
            elif len(witness) == 2:
                g, h = witness
                g = sp.sympify(g)
                h = sp.sympify(h)
                f = g * y + h
            else:
                return [False, False, False, False]
        else:
            f = sp.sympify(witness)
            syms = list(f.free_symbols)
            main_var = y if y in syms else (x if x in syms else y)
            f_poly = sp.Poly(f, main_var)
            g = f_poly.LC()
            h = f.subs(main_var, 0)
            
        g = sp.sympify(g)
        h = sp.sympify(h)
        f = sp.sympify(f)
        
        # H1: K is a field
        # We evaluate polynomials over the rationals (Q), which is a field.
        h1 = True
        
        # H2: g(x) and h(x) are relatively prime polynomials in K[x]
        gcd_gh = sp.gcd(g, h)
        h2 = bool(sp.simplify(gcd_gh).is_constant() and gcd_gh != 0)
        
        # H3: g(x) is not the zero polynomial
        h3 = bool(sp.simplify(g) != 0)
        
        # ¬Q: f(x,y) is NOT irreducible in K[x,y]
        # A polynomial is reducible over a field if the sum of the exponents of its non-constant factors is > 1.
        factors = sp.factor_list(f)
        num_factors = sum(exp for factor, exp in factors[1])
        neg_q = bool(num_factors > 1)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: g and h are relatively prime polynomials over K",
    "H_3: g is not the zero polynomial",
    "¬Q: f is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3