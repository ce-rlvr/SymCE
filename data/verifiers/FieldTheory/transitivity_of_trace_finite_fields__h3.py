import sympy
from sympy import GF
from sympy.polys.polytools import Poly
from sympy.abc import x
from sympy.ntheory import factorint

def conditions(witness):
    try:
        q, k, m, P_coeffs, alpha_coeffs = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            # q must be a prime power
            h1 = len(factorint(q)) == 1
    except Exception:
        h1 = False

    # H_2: K is a finite field extension of F_q
    try:
        h2 = isinstance(k, int) and k >= 1
    except Exception:
        h2 = False

    # H_3: alpha is an element of L
    try:
        if not (isinstance(m, int) and m >= 1):
            h3 = False
        else:
            # L is represented as F_q[x] / (P(x)) where P is irreducible of degree m
            P = Poly(P_coeffs, x, domain=GF(q))
            if P.degree() != m or not P.is_irreducible:
                h3 = False
            else:
                alpha = Poly(alpha_coeffs, x, domain=GF(q))
                # alpha must be an element of L, so its degree should be less than m
                if alpha.degree() >= m:
                    h3 = False
                else:
                    h3 = True
    except Exception:
        h3 = False

    # Conclusion: Tr_{L/F_q}(alpha) = Tr_{K/F_q}(Tr_{L/K}(alpha))
    try:
        if m % k != 0:
            # If L is not an extension of K, Tr_{L/K} is undefined, so the equation fails.
            q_holds = False
        else:
            P = Poly(P_coeffs, x, domain=GF(q))
            alpha = Poly(alpha_coeffs, x, domain=GF(q))
            
            def poly_pow_mod(base, exp, mod_poly):
                res = Poly(1, x, domain=base.domain) % mod_poly
                base = base % mod_poly
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * base) % mod_poly
                    base = (base * base) % mod_poly
                    exp //= 2
                return res

            # Compute Tr_{L/F_q}(alpha)
            tr_L_Fq = Poly(0, x, domain=GF(q))
            for i in range(m):
                term = poly_pow_mod(alpha, q**i, P)
                tr_L_Fq = (tr_L_Fq + term) % P
                
            # Compute Tr_{L/K}(alpha)
            tr_L_K = Poly(0, x, domain=GF(q))
            for i in range(m // k):
                term = poly_pow_mod(alpha, (q**k)**i, P)
                tr_L_K = (tr_L_K + term) % P
                
            # Compute Tr_{K/F_q}(Tr_{L/K}(alpha))
            tr_K_Fq_Tr_L_K = Poly(0, x, domain=GF(q))
            for j in range(k):
                term = poly_pow_mod(tr_L_K, q**j, P)
                tr_K_Fq_Tr_L_K = (tr_K_Fq_Tr_L_K + term) % P
                
            q_holds = (tr_L_Fq == tr_K_Fq_Tr_L_K)
    except Exception:
        q_holds = False

    neg_q = not q_holds

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: K is a finite field extension of F_q",
    "H_3: alpha is an element of L",
    "¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3