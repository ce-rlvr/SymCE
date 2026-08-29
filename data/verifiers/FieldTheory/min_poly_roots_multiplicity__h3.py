import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness can be a tuple (p, alpha) where p is a polynomial and alpha is a root,
    or just a polynomial p (in which case alpha is not strictly checked).
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            p = witness[0]
            alpha = witness[1]
            provided_alpha = True
        else:
            p = witness
            alpha = 0
            provided_alpha = False
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    # We use the field of rational numbers (QQ) as F.
    try:
        poly_p = sp.Poly(p, x, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    # H_2: alpha is an algebraic element over F
    try:
        # An expression with no free symbols can be evaluated to a constant,
        # representing an algebraic number in this context.
        h2 = len(sp.sympify(alpha).free_symbols) == 0
    except Exception:
        h2 = False

    # H_3: E is a splitting field of p(x) over F
    # If alpha was provided, we verify that p(alpha) == 0 to ensure the intended connection.
    # Otherwise, we just ensure p(x) is a non-constant polynomial (which always has a splitting field).
    try:
        if provided_alpha:
            expr_p = sp.sympify(p)
            if isinstance(expr_p, sp.Poly):
                expr_p = expr_p.as_expr()
            h3 = sp.simplify(expr_p.subs(x, alpha)) == 0
        else:
            h3 = poly_p.degree() >= 1
    except Exception:
        h3 = False

    # ¬Q: Not all roots of p(x) in E have the same multiplicity
    try:
        # Factorizing over QQ gives irreducible factors.
        # In characteristic 0, irreducible polynomials are separable (have distinct roots).
        # Thus, the multiplicity of any root in the splitting field is exactly 
        # the multiplicity of its minimal polynomial in the factorization of p(x).
        factors = sp.factor_list(poly_p)
        multiplicities = [mult for factor, mult in factors[1]]
        neg_q = len(set(multiplicities)) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: E is a splitting field of p(x) over F",
    "¬Q: Not all roots of p(x) in E have the same multiplicity"
]

N_HYP = 3
NEG_Q_INDEX = 3