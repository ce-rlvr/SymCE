import math
from sympy import Poly, isprime
from sympy.abc import x

def pow_poly(base, exp, mod, p):
    res = Poly(1, x, domain=f'GF({p})')
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

def trace(E_deg, F_deg, alpha_poly, p, min_poly):
    if E_deg % F_deg != 0:
        raise ValueError("Not an extension")
    deg = E_deg // F_deg
    res = Poly(0, x, domain=f'GF({p})')
    current = alpha_poly % min_poly
    res = (res + current) % min_poly
    for _ in range(1, deg):
        current = pow_poly(current, p**F_deg, min_poly, p)
        res = (res + current) % min_poly
    return res

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            q_deg = int(witness['q_deg'])
            k_deg = int(witness['k_deg'])
            l_deg = int(witness['l_deg'])
            min_poly_expr = witness['min_poly']
            alpha_expr = witness['alpha']
        elif hasattr(witness, 'p'):
            p = int(witness.p)
            q_deg = int(witness.q_deg)
            k_deg = int(witness.k_deg)
            l_deg = int(witness.l_deg)
            min_poly_expr = witness.min_poly
            alpha_expr = witness.alpha
        else:
            p, q_deg, k_deg, l_deg, min_poly_expr, alpha_expr = witness
            p = int(p)
            q_deg = int(q_deg)
            k_deg = int(k_deg)
            l_deg = int(l_deg)
    except Exception:
        return [False, False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        h1 = isprime(p) and q_deg >= 1
    except Exception:
        h1 = False

    # H_2: L is a finite field extension of K
    try:
        if not (k_deg >= 1 and l_deg >= 1 and l_deg % k_deg == 0):
            h2 = False
        else:
            poly = Poly(min_poly_expr, x, domain=f'GF({p})')
            h2 = poly.degree() == l_deg and poly.is_irreducible
    except Exception:
        h2 = False

    # H_3: alpha is an element of L
    try:
        alpha_poly = Poly(alpha_expr, x, domain=f'GF({p})')
        h3 = alpha_poly.is_zero or alpha_poly.degree() < l_deg
    except Exception:
        h3 = False

    # ¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))
    try:
        if l_deg % q_deg != 0:
            q_holds = False
        else:
            poly = Poly(min_poly_expr, x, domain=f'GF({p})')
            alpha_poly = Poly(alpha_expr, x, domain=f'GF({p})')
            lhs = trace(l_deg, q_deg, alpha_poly, p, poly)
            
            inner_trace = trace(l_deg, k_deg, alpha_poly, p, poly)
            
            if k_deg % q_deg != 0:
                q_holds = False
            else:
                rhs = trace(k_deg, q_deg, inner_trace, p, poly)
                q_holds = (lhs == rhs)
        neg_q = not q_holds
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: L is a finite field extension of K",
    "H_3: alpha is an element of L",
    "¬Q: Tr_{L/F_q}(alpha) != Tr_{K/F_q}(Tr_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3