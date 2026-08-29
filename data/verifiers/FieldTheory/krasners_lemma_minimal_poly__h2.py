import sympy
from sympy import Poly, diff, oo, isprime
from sympy.abc import x, t

# Top-level setup
# The witness can use x and t to define polynomials over F_p((t)).

def conditions(witness):
    try:
        p = witness['p']
        K_str = witness['K']
        poly_alpha = witness['poly_alpha']
        beta = witness['beta']
        r = witness['r']
        dist = witness['dist']
    except Exception:
        return [False] * 5

    # H_1: K is a field complete with respect to a non-archimedean absolute value
    try:
        h1 = bool((K_str == 'F_p((t))') and isprime(p))
    except Exception:
        h1 = False

    # H_2: m_α(x) is the minimal polynomial of α over K
    try:
        # Check Eisenstein criterion at t over F_p to ensure irreducibility
        P = Poly(poly_alpha, x)
        coeffs = P.all_coeffs()
        
        is_monic_mod_p = (Poly(coeffs[0], t).eval(0) % p != 0)
        
        div_by_t = True
        for c in coeffs[1:]:
            if Poly(c, t).eval(0) % p != 0:
                div_by_t = False
                break
                
        c_last = Poly(coeffs[-1], t)
        not_div_by_t2 = (c_last.coeff_monomial(t) % p != 0)
        
        h2 = bool(is_monic_mod_p and div_by_t and not_div_by_t2)
    except Exception:
        h2 = False

    # H_3: r is the minimum distance between α and any of its distinct Galois conjugates
    try:
        # If the formal derivative is 0 mod p, there are no distinct conjugates, so r = oo
        P_diff = Poly(diff(poly_alpha, x), x)
        diff_is_zero = True
        for c in P_diff.all_coeffs():
            for coeff in Poly(c, t).all_coeffs():
                if coeff % p != 0:
                    diff_is_zero = False
                    break
        
        h3 = bool(diff_is_zero and (r == oo))
    except Exception:
        h3 = False

    # H_4: the distance between α and β is strictly less than r
    try:
        h4 = bool(dist < r)
    except Exception:
        h4 = False

    # neg_Q: α ∉ K(β)
    try:
        deg = Poly(poly_alpha, x).degree()
        if hasattr(beta, 'free_symbols'):
            beta_in_K = (x not in beta.free_symbols)
        else:
            beta_in_K = isinstance(beta, (int, float))
        # If beta is in K, K(beta) = K. Since deg(m_alpha) > 1, alpha is not in K.
        h5 = bool(beta_in_K and (deg > 1))
    except Exception:
        h5 = False

    return [h1, h2, h3, h4, h5]

CONDITION_LABELS = [
    "H_1: K is a field complete with respect to a non-archimedean absolute value",
    "H_2: m_α(x) is the minimal polynomial of α over K",
    "H_3: r is the minimum distance between α and any of its distinct Galois conjugates",
    "H_4: the distance between α and β is strictly less than r",
    "¬Q: α ∉ K(β)"
]

N_HYP = 4
NEG_Q_INDEX = 4