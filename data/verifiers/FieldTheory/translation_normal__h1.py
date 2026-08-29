import sympy
from sympy import Symbol, minpoly, factor_list, Poly, I, sqrt, Rational, root
from sympy.abc import x

def conditions(witness):
    """
    witness is expected to be a dictionary with keys 'F', 'K', 'E'
    containing lists of algebraic numbers (SymPy expressions) generating the fields.
    Example: {'F': [], 'K': [root(2, 3)], 'E': []}
    """
    if isinstance(witness, dict):
        F = witness.get('F', [])
        K = witness.get('K', [])
        E = witness.get('E', [])
    elif isinstance(witness, tuple) and len(witness) == 3:
        F, K, E = witness
    else:
        return [False, False, False]

    def is_algebraic(gens):
        for g in gens:
            try:
                minpoly(g, x)
            except Exception:
                return False
        return True

    def get_minpoly_over_field(alpha, field_gens):
        p = minpoly(alpha, x)
        if not field_gens:
            return Poly(p, x)
        factors = factor_list(p, extension=field_gens)[1]
        for fac, mult in factors:
            if isinstance(fac, Poly):
                fac_expr = fac.as_expr()
            else:
                fac_expr = fac
            val = fac_expr.subs(x, alpha)
            try:
                cval = complex(val.evalf(50))
                if abs(cval) < 1e-20:
                    return Poly(fac_expr, x)
            except Exception:
                pass
        for fac, mult in factors:
            if isinstance(fac, Poly):
                fac_expr = fac.as_expr()
            else:
                fac_expr = fac
            val = fac_expr.subs(x, alpha)
            if sympy.simplify(val) == 0:
                return Poly(fac_expr, x)
        raise ValueError("No factor has alpha as root")

    # H1: E/F is a field extension (F is a subfield of E)
    h1 = True
    try:
        for f in F:
            mp = get_minpoly_over_field(f, E)
            if mp.degree() > 1:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: K and E are subfields of a common overfield L
    # In our representation, all valid algebraic numbers share the common overfield QQ-bar (or C).
    h2 = False
    try:
        if is_algebraic(F) and is_algebraic(K) and is_algebraic(E):
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: KE is NOT a normal extension of E
    neg_q = False
    try:
        # The generators of KE are the union of generators of K and E
        KE = []
        for gen in K + E:
            if gen not in KE:
                KE.append(gen)
                
        is_normal = True
        for k in K:
            mp = get_minpoly_over_field(k, E)
            if not KE:
                factors = factor_list(mp.as_expr())[1]
            else:
                factors = factor_list(mp.as_expr(), extension=KE)[1]
            
            for fac, mult in factors:
                if isinstance(fac, Poly):
                    deg = fac.degree()
                else:
                    deg = Poly(fac, x).degree()
                if deg > 1:
                    is_normal = False
                    break
            if not is_normal:
                break
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: K and E are subfields of a common overfield L",
    "¬Q: The compositum KE is not a normal extension of E"
]

N_HYP = 2
NEG_Q_INDEX = 2