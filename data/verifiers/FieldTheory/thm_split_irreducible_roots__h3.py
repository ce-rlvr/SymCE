import sympy
from sympy import Symbol, Poly, RootOf, factor_list

x = Symbol('x')

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        
        minpoly_K, g = witness
        
        if not hasattr(minpoly_K, 'free_symbols') or not hasattr(g, 'free_symbols'):
            return [False, False, False, False]

        # H1: F is a field (F=QQ, minpoly_K and g in QQ polynomials)
        try:
            if not minpoly_K.free_symbols.issubset({x}) or not g.free_symbols.issubset({x}):
                h1 = False
            else:
                poly_min = Poly(minpoly_K, x, domain='QQ')
                poly_g = Poly(g, x, domain='QQ')
                # Limit degrees to ensure fast execution
                if poly_min.degree() > 5 or poly_g.degree() > 10:
                    h1 = False
                elif poly_min.degree() < 1:
                    h1 = False
                else:
                    h1 = True
        except Exception:
            h1 = False

        if not h1:
            return [False, False, False, False]

        # H2: K is a splitting field of some polynomial over F
        try:
            alpha = RootOf(poly_min, 0)
            if alpha.is_Rational:
                factors_min = factor_list(minpoly_K)
            else:
                factors_min = factor_list(minpoly_K, extension=alpha)
            # K = QQ(alpha) is a splitting field iff minpoly_K splits completely in K
            h2 = all(Poly(fac, x).degree() == 1 for fac, mult in factors_min[1])
        except Exception:
            h2 = False

        # H3: g has at least one root in K
        try:
            if alpha.is_Rational:
                factors_g = factor_list(g)
            else:
                factors_g = factor_list(g, extension=alpha)
            # A linear factor over K corresponds to a root in K
            h3 = any(Poly(fac, x).degree() == 1 for fac, mult in factors_g[1])
        except Exception:
            h3 = False

        # neg_Q: g does NOT split completely into linear factors over K
        try:
            # If any irreducible factor over K has degree > 1, it does not split completely
            neg_q = not all(Poly(fac, x).degree() == 1 for fac, mult in factors_g[1])
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a splitting field of some polynomial over F",
    "H_3: g has at least one root in K",
    "¬Q: g does NOT split completely into linear factors over K"
]

N_HYP = 3
NEG_Q_INDEX = 3