import sympy
from sympy.abc import x

def conditions(witness):
    try:
        f_expr, q = witness
    except Exception:
        return [False, False]
        
    # H1: f(x) is a non-zero polynomial in F_q[x]
    try:
        f_poly = sympy.Poly(f_expr, x)
        q_int = int(q)
        is_zero_mod_q = True
        for c in f_poly.all_coeffs():
            if int(c) % q_int != 0:
                is_zero_mod_q = False
                break
        h1 = not is_zero_mod_q
    except Exception:
        h1 = False

    # Conclusion: The number of distinct roots of f(x) in F_q is equal to the degree of \gcd(f(x), x^q - x)
    try:
        q_int = int(q)
        distinct_roots = 0
        for a in range(q_int):
            val = f_poly.eval(a)
            if int(val) % q_int == 0:
                distinct_roots += 1
                
        try:
            gcd_expr = sympy.gcd(f_expr, x**q_int - x, modulus=q_int)
            gcd_poly = sympy.Poly(gcd_expr, x)
            deg_gcd = gcd_poly.degree()
            if deg_gcd == -sympy.oo:
                deg_gcd = -1
            q_holds = (distinct_roots == deg_gcd)
        except Exception:
            # If GCD cannot be computed (e.g., due to non-invertible elements in Z/qZ),
            # the degree is undefined, so the equality fails.
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial over F_q",
    "not Q: The number of distinct roots of f in F_q is NOT equal to the degree of gcd"
]

N_HYP = 1
NEG_Q_INDEX = 1