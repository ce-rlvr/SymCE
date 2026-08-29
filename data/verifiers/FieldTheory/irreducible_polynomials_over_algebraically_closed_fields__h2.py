import sympy
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a polynomial expression `p` (implicitly over CC),
    or a tuple `(K, p)` where K is the field and p is the polynomial.
    """
    # H_1: Let K be an algebraically closed field.
    if isinstance(witness, tuple) and len(witness) == 2:
        K, p = witness
        try:
            # In SymPy, the standard algebraically closed field is the Complex numbers.
            if K == sympy.S.Complexes or str(K) in ["CC", "C", "Complexes", "AlgebraicallyClosedField"]:
                h1 = True
            else:
                h1 = False
        except Exception:
            h1 = False
    else:
        p = witness
        h1 = True  # Implicitly assume K = CC if only the polynomial is provided

    # H_2: p(x) is irreducible over K.
    h2 = False
    try:
        p_expr = sympy.sympify(p)
        free_vars = p_expr.free_symbols
        
        if len(free_vars) == 1:
            # Over an algebraically closed field, a polynomial in one variable 
            # is irreducible if and only if its degree is exactly 1.
            var = list(free_vars)[0]
            if sympy.degree(p_expr, var) == 1:
                h2 = True
        elif len(free_vars) > 1:
            poly = sympy.Poly(p_expr)
            # Any homogeneous polynomial in 2 variables of degree > 1 factors over an algebraically closed field.
            if poly.is_homogeneous and len(free_vars) == 2 and poly.total_degree() > 1:
                h2 = False
            else:
                # For multivariate polynomials, we use irreducibility over QQ(I) as a fast, 
                # practical heuristic for absolute irreducibility over CC.
                f_list = sympy.factor_list(p_expr, extension=sympy.I)
                if len(f_list[1]) == 1 and f_list[1][0][1] == 1:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: The degree of p(x) is NOT exactly 1.
    neg_q = False
    try:
        p_expr = sympy.sympify(p)
        poly = sympy.Poly(p_expr)
        if poly.total_degree() != 1:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: p(x) is irreducible over K",
    "¬Q: The degree of p(x) is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2