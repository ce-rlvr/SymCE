import sympy as sp

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the Equal Degree Factorization Theorem
    when the hypothesis "f(x) is irreducible" is dropped.
    
    The witness is expected to be a tuple: (min_poly_expr, f_expr)
    where:
      - min_poly_expr is a polynomial in x over QQ defining the extension E = QQ(alpha).
      - f_expr is a polynomial in x over QQ (representing f(x) in F[x]).
    """
    try:
        min_poly_expr, f_expr = witness
    except Exception:
        return [False, False]
        
    # Check H_1: E/F is a normal field extension
    try:
        min_poly = sp.Poly(min_poly_expr, x, domain='QQ')
        if not min_poly.is_irreducible:
            h1 = False
        elif min_poly.degree() <= 1:
            # Degree 1 means E = QQ, which is trivially a normal extension of QQ
            h1 = True
        else:
            # For E = QQ(alpha) to be normal over QQ, min_poly must split completely in E
            alpha = sp.RootOf(min_poly_expr, x, 0)
            factors = sp.factor_list(min_poly_expr, x, extension=alpha)
            h1 = all(sp.Poly(fac, x).degree() == 1 for fac, exp in factors[1])
    except Exception:
        h1 = False

    # Check ¬Q: Not all irreducible factors of f(x) over E have the same degree
    try:
        min_poly = sp.Poly(min_poly_expr, x, domain='QQ')
        
        if min_poly.degree() <= 1:
            factors_f = sp.factor_list(f_expr, x, domain='QQ')
        else:
            alpha = sp.RootOf(min_poly_expr, x, 0)
            factors_f = sp.factor_list(f_expr, x, extension=alpha)
            
        degrees = [sp.Poly(fac, x).degree() for fac, exp in factors_f[1]]
        
        if not degrees:
            neg_q = False
        else:
            # The conclusion fails if there are strictly more than 1 distinct degrees
            # among the irreducible factors of f(x) over E.
            neg_q = len(set(degrees)) > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: E/F is a normal field extension", "not Q: Not all irreducible factors of f(x) over E have the same degree"]
N_HYP = 1
NEG_Q_INDEX = 1