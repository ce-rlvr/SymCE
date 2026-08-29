import math
from sympy import totient, rem
from sympy.polys.numberfields import minpoly
from sympy.polys.specialpolys import cyclotomic_poly
from sympy.abc import x

# Top-level setup
# (No specific named bindings required for this Field Theory conjecture)

def conditions(witness):
    try:
        n, m, zeta_n, zeta_m = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: n and m are positive integers
    try:
        h1 = (int(n) == n) and (int(m) == m) and (n > 0) and (m > 0)
    except Exception:
        h1 = False
        
    # H2: n and m are coprime
    try:
        h2 = math.gcd(int(n), int(m)) == 1
    except Exception:
        h2 = False
        
    # H3: zeta_n is a primitive n-th root of unity
    try:
        poly_n = minpoly(zeta_n, x)
        h3 = (poly_n == cyclotomic_poly(int(n), x))
    except Exception:
        h3 = False
        
    # Conclusion: Q(zeta_n)Q(zeta_m) == Q(zeta_nm)
    try:
        poly_m = minpoly(zeta_m, x)
        m_int = int(m)
        
        # To prevent trivial non-cyclotomic counterexamples, we enforce the implicit
        # assumption that zeta_m is an m-th root of unity.
        is_m_root = (rem(x**m_int - 1, poly_m, x) == 0)
        
        if is_m_root:
            # If zeta_m is an m-th root of unity, the compositum equals the nm-th
            # cyclotomic field iff the degree of zeta_m is totient(m).
            q_holds = (poly_m.degree() == totient(m_int))
        else:
            # If zeta_m is not an m-th root of unity, we reject the witness by
            # evaluating the conclusion as True (so neg_q = False).
            q_holds = True
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: n and m are coprime",
    "H_3: ζ_n is a primitive n-th root of unity",
    "¬Q: The compositum field ℚ(ζ_n)ℚ(ζ_m) is not equal to ℚ(ζ_{nm})"
]

N_HYP = 3
NEG_Q_INDEX = 3