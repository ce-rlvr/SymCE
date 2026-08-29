import sympy as sp
from sympy.abc import x, X

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the conjecture.
    The witness should be a tuple (minpoly_expr, alpha_expr) where:
      - minpoly_expr is a SymPy expression in `x` representing the minimal polynomial of E/QQ.
      - alpha_expr is a SymPy expression in `x` representing the element alpha in E.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        minpoly_expr, alpha_expr = witness
    except Exception:
        return [False, False]
        
    # H1: E/F is a field extension of degree 2
    # We assume F = QQ. So minpoly_expr must be an irreducible polynomial of degree 2 over QQ.
    try:
        p = sp.Poly(minpoly_expr, x, domain='QQ')
        h1 = (p.degree() == 2) and p.is_irreducible
    except Exception:
        h1 = False
        
    # Conclusion: The minimal polynomial of alpha over F is x^2 - Tr(alpha)x + N(alpha)
    try:
        p = sp.Poly(minpoly_expr, x, domain='QQ')
        if p.degree() != 2:
            neg_q = False
        else:
            # Evaluate alpha_expr as a rational function in x
            alpha_expr = sp.sympify(alpha_expr)
            num, den = alpha_expr.as_numer_denom()
            
            # Invert denominator modulo the minimal polynomial
            s, t, g = sp.gcdex(den, minpoly_expr, x, domain='QQ')
            if sp.degree(g, x) > 0:
                neg_q = False
            else:
                # alpha = num * s / g mod p
                alpha_expr_mod = sp.expand((num * s) / g)
                alpha_poly = sp.Poly(alpha_expr_mod, x, domain='QQ')
                _, rem = alpha_poly.div(p)
                
                # Get coefficients alpha_1 and alpha_0 such that alpha = alpha_1 * x + alpha_0
                rem_coeffs = rem.all_coeffs()
                if len(rem_coeffs) == 2:
                    alpha_1, alpha_0 = rem_coeffs
                elif len(rem_coeffs) == 1:
                    alpha_1, alpha_0 = sp.S.Zero, rem_coeffs[0]
                else:
                    alpha_1, alpha_0 = sp.S.Zero, sp.S.Zero
                    
                # Get c_1 and c_0 from minpoly_expr = x^2 + a*x + b
                # x^2 = -a*x - b, so c_1 = -a, c_0 = -b
                p_coeffs = p.all_coeffs()
                lead = p_coeffs[0]
                a = p_coeffs[1] / lead
                b = p_coeffs[2] / lead
                c_1 = -a
                c_0 = -b
                
                # Trace and Norm of alpha in E/QQ
                Tr = 2*alpha_0 + alpha_1*c_1
                N = alpha_0**2 + alpha_0*alpha_1*c_1 - alpha_1**2*c_0
                
                # The polynomial given by the formula
                formula_poly = sp.Poly(X**2 - Tr*X + N, X, domain='QQ')
                
                # The actual minimal polynomial of alpha over QQ
                if alpha_1 == 0:
                    # If alpha is in QQ, its minimal polynomial has degree 1
                    actual_minpoly = sp.Poly(X - alpha_0, X, domain='QQ')
                else:
                    # If alpha is not in QQ, its minimal polynomial is the characteristic polynomial
                    actual_minpoly = formula_poly
                    
                # The conclusion fails if the actual minimal polynomial does not match the formula
                neg_q = (actual_minpoly != formula_poly)
                
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E/F is a field extension of degree 2",
    "¬Q: The minimal polynomial of alpha over F is not x^2 - Tr(alpha)x + N(alpha)"
]

N_HYP = 1
NEG_Q_INDEX = 1