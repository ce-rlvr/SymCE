import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
t = sp.Symbol('t')
x = sp.Symbol('x')
QQ = sp.QQ
Q_t = sp.QQ.frac_field(t)
Q_sqrt2 = sp.QQ.algebraic_field(sp.sqrt(2))

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        F, E, alpha = witness
    except Exception:
        return [False, False, False]
    
    # H1: The extension E/F is normal
    h1 = False
    try:
        if F == E:
            h1 = True
        elif getattr(E, 'is_FractionField', False) and E.domain == F:
            h1 = True
        elif getattr(E, 'is_AlgebraicField', False) and E.domain == F:
            # Degree 2 extensions are always normal
            if E.ext.degree() <= 2:
                h1 = True
    except Exception:
        pass

    # H2: alpha is an element of E
    h2 = False
    try:
        # If alpha can be coerced into E, it is an element of E
        E(alpha)
        h2 = True
    except Exception:
        pass

    # neg_Q: The minimal polynomial of alpha over F does not factor completely into linear polynomials over E
    neg_q = False
    try:
        poly = sp.minpoly(alpha, x, domain=F)
        factors = sp.factor_list(poly, domain=E)
        all_linear = all(f.degree() == 1 for f, m in factors[1])
        neg_q = not all_linear
    except Exception:
        # If minpoly raises an exception (e.g., NotAlgebraic), it does not exist,
        # so it does not factor completely into linear polynomials.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The extension E/F is normal",
    "H_2: alpha is an element of E",
    "¬Q: The minimal polynomial of alpha over F does not factor completely into linear polynomials over E"
]

N_HYP = 2
NEG_Q_INDEX = 2