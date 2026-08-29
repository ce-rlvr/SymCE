import sympy

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If F is a formally real field and α is algebraic over F, then F(α) is formally real."
    
    A valid witness is a minimal polynomial over Q (or an algebraic number) 
    that generates an extension field without any real embeddings.
    """
    # H_1: F is a formally real field
    # We assume F = Q, which is formally real. We verify the witness can be 
    # interpreted as a polynomial over Q.
    try:
        if isinstance(witness, (tuple, list)):
            poly_wit = witness[-1]
        else:
            poly_wit = witness
            
        # If the witness is an algebraic number (e.g., sympy.I), compute its minimal polynomial
        if isinstance(poly_wit, sympy.Expr) and not poly_wit.has(x):
            poly_expr = sympy.minpoly(poly_wit, x)
            p = sympy.Poly(poly_expr, x, domain='QQ')
        else:
            p = sympy.Poly(poly_wit, x, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    # H_2: α is algebraic over F
    # This requires the polynomial to be non-constant and irreducible over Q,
    # so that F[x]/(p) is a valid simple algebraic extension field F(α).
    try:
        if not h1:
            h2 = False
        else:
            h2 = bool(p.degree() > 0 and p.is_irreducible)
    except Exception:
        h2 = False

    # ¬Q: F(α) is NOT formally real
    # A number field F(α) is formally real if and only if it has at least one real embedding.
    # This is equivalent to its minimal polynomial having at least one real root.
    # Thus, it is NOT formally real iff the minimal polynomial has NO real roots.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            rr = sympy.real_roots(p)
            neg_q = len(rr) == 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a formally real field (assumed F=Q for rational polynomial)",
    "H_2: α is algebraic over F (witness is a non-constant irreducible polynomial)",
    "¬Q: F(α) is not formally real (minimal polynomial has no real roots)"
]

N_HYP = 2
NEG_Q_INDEX = 2