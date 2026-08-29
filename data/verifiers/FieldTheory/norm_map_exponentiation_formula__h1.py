import sympy as sp

# Top-level setup
x = sp.Symbol('x')

def conditions(witness):
    """
    witness is expected to be a tuple defining the fields and the element:
      (q, n, P_coeffs, alpha_coeffs) for an extension over QQ
    or
      (p, q, n, P_coeffs, alpha_coeffs) for an extension over GF(p)
      
    where:
      p: prime characteristic (if using finite field base)
      q: the parameter q in the theorem (which was supposed to be the base field size)
      n: degree of the extension
      P_coeffs: coefficients of the irreducible polynomial P(x) defining the extension
      alpha_coeffs: coefficients of alpha(x) in the extension field
    """
    try:
        if len(witness) == 4:
            q, n, P_coeffs, alpha_coeffs = witness
            domain = sp.QQ
        elif len(witness) == 5:
            p, q, n, P_coeffs, alpha_coeffs = witness
            p = int(p)
            domain = sp.GF(p)
        else:
            return [False, False, False]
            
        q = int(q)
        n = int(n)
    except Exception:
        return [False, False, False]
        
    # H_1: F_{q^n} is an extension field of degree n over F_q
    try:
        P = sp.Poly(P_coeffs, x, domain=domain)
        H1 = (P.degree() == n) and P.is_irreducible and (n >= 1)
    except Exception:
        H1 = False
        
    # H_2: \alpha is an element of F_{q^n}
    try:
        alpha = sp.Poly(alpha_coeffs, x, domain=domain)
        H2 = True
    except Exception:
        H2 = False
        
    # ¬Q: The norm N_{F_{q^n}/F_q}(\alpha) is not equal to \alpha^{(q^n-1)/(q-1)}
    try:
        if not P.is_monic:
            P = P.monic()
            
        alpha = alpha.rem(P)
        
        # Compute the norm of alpha down to the base field
        if alpha.is_zero:
            norm_val = domain.zero
        else:
            norm_val = P.resultant(alpha)
            
        # Compute the exponent (q^n - 1) / (q - 1) safely as sum_{i=0}^{n-1} q^i
        E = sum(q**i for i in range(n))
        
        res_poly = sp.Poly(1, x, domain=domain)
        base_poly = alpha
        
        exp = E
        if exp < 0:
            base_poly = base_poly.invert(P)
            exp = -exp
            
        # Exponentiation by squaring in the extension field
        while exp > 0:
            if exp % 2 == 1:
                res_poly = (res_poly * base_poly).rem(P)
            base_poly = (base_poly * base_poly).rem(P)
            exp //= 2
            
        expected_poly = sp.Poly(norm_val, x, domain=domain)
        
        # The conclusion fails if the computed power does not equal the norm
        neg_Q = (res_poly != expected_poly)
    except Exception:
        neg_Q = False
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: F_{q^n} is an extension field of degree n over F_q",
    "H_2: \\alpha is an element of F_{q^n}",
    "¬Q: The norm N_{F_{q^n}/F_q}(\\alpha) is not equal to \\alpha^{(q^n-1)/(q-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2