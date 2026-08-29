import sympy
from sympy import Dummy, Poly, lcm, gcd, fraction, minpoly

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        F, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H1: α is an element in an extension field of F
    try:
        # F should be a ring (like ZZ or QQ) that can be embedded in a field
        h1 = hasattr(F, 'is_Ring') and F.is_Ring
        if h1:
            # alpha should be a valid number (element of CC, which is an extension field)
            h1 = hasattr(alpha, 'is_number') and alpha.is_number
    except Exception:
        h1 = False
        
    # H2: α is algebraic over F
    try:
        x = Dummy('x')
        p_QQ = minpoly(alpha, x)
        h2 = p_QQ is not None and Poly(p_QQ, x).degree() >= 1
    except Exception:
        h2 = False
        
    # neg_Q: The minimal polynomial of α over F has degree 1 iff α ∈ F
    try:
        x = Dummy('x')
        p_QQ = minpoly(alpha, x)
        
        if F == ZZ:
            # The minimal polynomial over ZZ is the primitive polynomial in ZZ[x]
            p_poly = Poly(p_QQ, x, domain='QQ')
            coeffs = p_poly.all_coeffs()
            denoms = [fraction(c)[1] for c in coeffs]
            l = 1
            for d in denoms:
                l = lcm(l, d)
            p_ZZ = p_QQ * l
            g = 0
            for c in Poly(p_ZZ, x).all_coeffs():
                g = gcd(g, c)
            p_F = p_ZZ / g
            alpha_in_F = (alpha.is_integer == True)
        elif F == QQ:
            p_F = p_QQ
            alpha_in_F = (alpha.is_rational == True)
        else:
            # Fallback for other domains
            p_poly = Poly(p_QQ, x, domain=F)
            p_F = p_poly.as_expr()
            try:
                F.from_sympy(alpha)
                alpha_in_F = True
            except Exception:
                alpha_in_F = False
                
        deg_is_1 = (Poly(p_F, x).degree() == 1)
        
        # The conclusion fails if the equivalence does not hold
        neg_q = (deg_is_1 != alpha_in_F)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: α is an element in an extension field of F",
    "H_2: α is algebraic over F",
    "¬Q: The minimal polynomial of α over F has degree 1 iff α ∈ F fails"
]

N_HYP = 2
NEG_Q_INDEX = 2