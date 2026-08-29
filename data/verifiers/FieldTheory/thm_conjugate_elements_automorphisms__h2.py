import sympy
from sympy import Poly, QQ, CRootOf, Matrix
from sympy.abc import x, y

# Top-level setup for the verifier
# The witness is expected to be a tuple: (P_coeffs, alpha_coeffs, beta_coeffs)
# where:
#   - P_coeffs: list of rational coefficients for the irreducible polynomial P(x) over QQ.
#               This defines the field extension E = QQ[x]/(P(x)) = QQ(theta).
#   - alpha_coeffs: list of rational coefficients for alpha as a polynomial in theta.
#   - beta_coeffs: list of rational coefficients for beta as a polynomial in theta.

def conditions(witness):
    try:
        P_coeffs, alpha_coeffs, beta_coeffs = witness
        P = Poly(P_coeffs, x, domain=QQ)
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field. 
    # We use F = QQ, which is always a field.
    # We also require E to be a valid field extension, so P must be irreducible over QQ.
    try:
        h1 = P.is_irreducible
    except Exception:
        h1 = False
        
    # H_2: \alpha and \beta are elements of E that are algebraic over F.
    # By construction, any polynomial in theta with rational coefficients is in E 
    # and is algebraic over QQ. We just verify they form valid polynomials.
    try:
        alpha_poly = Poly(alpha_coeffs, x, domain=QQ)
        beta_poly = Poly(beta_coeffs, x, domain=QQ)
        h2 = True
    except Exception:
        h2 = False
        
    # \neg Q: \alpha and \beta share the same minimal polynomial over F 
    # BUT there is NO automorphism \sigma \in Aut(E/F) such that \sigma(\alpha) = \beta.
    try:
        # Helper to compute the minimal polynomial of an element A(theta) in QQ[x]/(P(x))
        def minpoly_mod(A_poly, P_poly):
            d = P_poly.degree()
            vecs = []
            curr = Poly(1, x, domain=QQ)
            for i in range(d + 1):
                c = curr.all_coeffs()
                c = [QQ(0)] * (d - len(c)) + c
                c.reverse()  # c[0] is the constant term
                vecs.append(c)
                M = Matrix(vecs).T
                ns = M.nullspace()
                if ns:
                    ns_vec = ns[0]
                    lc = ns_vec[-1]
                    res = [val / lc for val in ns_vec]
                    res.reverse()
                    return Poly(res, x, domain=QQ)
                curr = (curr * A_poly) % P_poly
            return None

        min_alpha = minpoly_mod(alpha_poly, P)
        min_beta = minpoly_mod(beta_poly, P)
        
        same_minpoly = (min_alpha is not None) and (min_beta is not None) and (min_alpha == min_beta)
        
        # Find all automorphisms of E over QQ.
        # An automorphism maps theta to another root of P(x) that is also in E.
        theta = CRootOf(P, 0)
        K = QQ.algebraic_field(theta)
        P_y = Poly(P.as_expr().subs(x, y), y, domain=K)
        roots_dict = P_y.roots()
        
        exists_auto = False
        
        # Evaluate beta in K
        beta_val = K.zero
        theta_K = K(theta)
        theta_pow = K.one
        coeffs_b = beta_poly.all_coeffs()
        coeffs_b.reverse()
        for c in coeffs_b:
            c_rat = sympy.Rational(c.numerator, c.denominator)
            beta_val = beta_val + K(c_rat) * theta_pow
            theta_pow = theta_pow * theta_K
            
        # Check if any automorphism maps alpha to beta
        for r in roots_dict.keys():
            alpha_r = K.zero
            r_pow = K.one
            coeffs_a = alpha_poly.all_coeffs()
            coeffs_a.reverse()
            for c in coeffs_a:
                c_rat = sympy.Rational(c.numerator, c.denominator)
                alpha_r = alpha_r + K(c_rat) * r_pow
                r_pow = r_pow * r
                
            if alpha_r == beta_val:
                exists_auto = True
                break
                
        # The conclusion states: same_minpoly <=> exists_auto
        # The negation is that this equivalence fails (i.e., they have different boolean values)
        neg_q = (same_minpoly != exists_auto)
        
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: \\alpha and \\beta are elements of E that are algebraic over F",
    "¬Q: \\alpha and \\beta share the same minimal polynomial over F but no automorphism maps \\alpha to \\beta"
]

N_HYP = 2
NEG_Q_INDEX = 2