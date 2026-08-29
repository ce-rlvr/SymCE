import sympy as sp

x = sp.Symbol('x')
t = sp.Symbol('t')

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, F, alpha), check if it is a valid counterexample to the conjecture.
    The witness should be a tuple: (R, F, alpha) where R is a SymPy domain, F is a SymPy domain,
    and alpha is an element or matrix.
    """
    try:
        R, F, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is an integrally closed integral domain
    try:
        h1 = getattr(R, 'is_Domain', False) and getattr(R, 'is_UFD', False)
    except Exception:
        h1 = False

    # H2: F is the field of fractions of R
    try:
        h2 = (F == R.get_field())
    except Exception:
        h2 = False

    # H3: alpha is integral over R
    try:
        if isinstance(alpha, sp.Matrix):
            charpoly = alpha.charpoly(x)
            h3 = all(c in R for c in charpoly.all_coeffs())
        else:
            mp = sp.minpoly(alpha, x, domain=F)
            h3 = all(c in R for c in sp.Poly(mp, x).all_coeffs())
    except Exception:
        h3 = False

    # neg_Q: The minimal polynomial of alpha over F does NOT lie in R[x]
    try:
        if isinstance(alpha, sp.Matrix):
            charpoly = alpha.charpoly(x)
            factors = sp.factor_list(charpoly, domain=F)[1]
            min_poly = sp.Poly(1, x, domain=F)
            for factor, exp in factors:
                base_poly = sp.Poly(1, x, domain=F)
                for other_factor, other_exp in factors:
                    if other_factor != factor:
                        base_poly *= sp.Poly(other_factor, x, domain=F) ** other_exp
                
                for i in range(1, exp + 1):
                    test_poly = base_poly * (sp.Poly(factor, x, domain=F) ** i)
                    coeffs = test_poly.all_coeffs()
                    mat_val = sp.zeros(alpha.rows, alpha.cols)
                    for j, c in enumerate(reversed(coeffs)):
                        mat_val += c * (alpha ** j)
                    if mat_val.is_zero_matrix:
                        min_poly *= sp.Poly(factor, x, domain=F) ** i
                        break
            neg_q = not all(c in R for c in min_poly.all_coeffs())
        else:
            mp = sp.minpoly(alpha, x, domain=F)
            neg_q = not all(c in R for c in sp.Poly(mp, x).all_coeffs())
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = ["H_1: R is an integrally closed integral domain", "H_2: F is the field of fractions of R", "H_3: alpha is integral over R", "not Q: The minimal polynomial of alpha over F does not lie in the polynomial ring over R"]

N_HYP = 3
NEG_Q_INDEX = 3