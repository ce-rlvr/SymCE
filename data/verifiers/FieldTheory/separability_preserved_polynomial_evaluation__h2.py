import sympy as sp

t, X = sp.symbols('t X')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (p, m_poly, f_poly)
    where:
      - p is a prime number (characteristic of the field).
      - m_poly is an irreducible monic polynomial in X over F_p[t], defining the extension L = K(alpha).
      - f_poly is a polynomial in X over F_p[t], representing f in K[x].
    """
    try:
        p, m_poly, f_poly = witness
    except Exception:
        return [False, False, False]
        
    try:
        p = int(p)
        if not sp.isprime(p):
            h1_ok = False
        else:
            m_expr = sp.sympify(m_poly, locals={'X': X, 't': t})
            if not m_expr.free_symbols.issubset({X, t}):
                h1_ok = False
            else:
                poly_m = sp.Poly(m_expr, X, t, domain=sp.GF(p))
                if poly_m.degree(X) < 1:
                    h1_ok = False
                elif sp.Poly(m_expr, X).LC() != 1:
                    h1_ok = False
                else:
                    facs = sp.factor_list(m_expr, X, t, domain=sp.GF(p))
                    h1_ok = (len(facs[1]) == 1 and facs[1][0][1] == 1)
    except Exception:
        h1_ok = False

    try:
        f_expr = sp.sympify(f_poly, locals={'X': X, 't': t})
        if not f_expr.free_symbols.issubset({X, t}):
            h2_ok = False
        else:
            poly_f = sp.Poly(f_expr, X, t, domain=sp.GF(p))
            h2_ok = True
    except Exception:
        h2_ok = False

    try:
        Y = sp.Symbol('Y')
        R = sp.resultant(m_expr, Y - f_expr, X)
        R_poly = sp.Poly(R, Y, t, domain=sp.GF(p))
        R_expr = R_poly.as_expr()
        
        facs = sp.factor_list(R_expr, Y, t, domain=sp.GF(p))
        g = None
        for fac, mult in facs[1]:
            if sp.Poly(fac, Y).degree() > 0:
                g = fac
                break
                
        if g is None:
            neg_q_ok = False
        else:
            g_diff = sp.diff(g, Y)
            g_diff_poly = sp.Poly(g_diff, Y, t, domain=sp.GF(p))
            neg_q_ok = g_diff_poly.is_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L over K is a field extension",
    "H_2: f is a polynomial over K",
    "¬Q: f(alpha) is not separable over K"
]

N_HYP = 2
NEG_Q_INDEX = 2