import sympy

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, Psi_n = witness
                try:
                    n_val = int(n)
                    Phi_n = sympy.cyclotomic_poly(n_val, x)
                except Exception:
                    Phi_n = None
            elif len(witness) == 3:
                n, Phi_n, Psi_n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: n is an integer strictly greater than 2
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val > 2)
    except Exception:
        h1 = False

    # H2: Phi_n(x) is the n-th cyclotomic polynomial
    try:
        if h1 and Phi_n is not None:
            expected_Phi_n = sympy.cyclotomic_poly(n_val, x)
            h2 = sympy.expand(Phi_n - expected_Phi_n) == 0
        else:
            h2 = False
    except Exception:
        h2 = False

    # Conclusion: degree of Psi_n(x) is phi(n)/2, and Phi_n(x) = x^{phi(n)/2} Psi_n(x + x^{-1})
    try:
        if not h1 or Phi_n is None:
            neg_q = False
        else:
            phi_n = sympy.totient(n_val)
            deg_expected = phi_n // 2
            
            Psi_n_expr = sympy.sympify(Psi_n)
            
            if not Psi_n_expr.is_polynomial(x):
                q = False
            else:
                deg_Psi = sympy.degree(Psi_n_expr, x)
                deg_ok = (deg_Psi == deg_expected)
                
                rhs = (x**deg_expected) * Psi_n_expr.subs(x, x + 1/x)
                relation_ok = sympy.expand(Phi_n - rhs) == 0
                
                q = deg_ok and relation_ok
                
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: The degree of Psi_n(x) is not phi(n)/2, or Phi_n(x) != x^{phi(n)/2} Psi_n(x + x^{-1})"
]

N_HYP = 2
NEG_Q_INDEX = 2