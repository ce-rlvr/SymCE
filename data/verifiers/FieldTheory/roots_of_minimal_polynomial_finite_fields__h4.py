import sympy
from sympy import Poly, GF, isprime
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: alpha is an element of an extension field",
    "H_3: m(x) is the minimal polynomial of alpha over F_q",
    "¬Q: The roots of m(x) are not exactly the d distinct elements"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        q = witness['q']
        h1 = isprime(q)
    except Exception:
        h1 = False

    try:
        q = witness['q']
        n = witness['n']
        P_coeffs = witness['P']
        alpha_coeffs = witness['alpha']
        
        P_poly = Poly(P_coeffs, x, domain=GF(q))
        h2_1 = P_poly.degree() == n and P_poly.is_irreducible
        
        alpha_poly = Poly(alpha_coeffs, x, domain=GF(q))
        h2_2 = alpha_poly.degree() < n or alpha_poly.is_zero
        
        h2 = bool(h2_1 and h2_2)
    except Exception:
        h2 = False

    try:
        q = witness['q']
        P_coeffs = witness['P']
        alpha_coeffs = witness['alpha']
        m_coeffs = witness['m']
        
        P_poly = Poly(P_coeffs, x, domain=GF(q))
        alpha_poly = Poly(alpha_coeffs, x, domain=GF(q))
        m_poly = Poly(m_coeffs, x, domain=GF(q))
        
        h3_1 = int(m_poly.LC()) == 1
        h3_2 = m_poly.is_irreducible
        
        res = Poly(0, x, domain=GF(q))
        alpha_pow = Poly(1, x, domain=GF(q))
        m_list = [int(c) for c in m_poly.all_coeffs()]
        m_list.reverse()
        for c in m_list:
            term = alpha_pow.mul(Poly(c, x, domain=GF(q)))
            res = res.add(term).rem(P_poly)
            alpha_pow = alpha_pow.mul(alpha_poly).rem(P_poly)
            
        h3_3 = res.is_zero
        h3 = bool(h3_1 and h3_2 and h3_3)
    except Exception:
        h3 = False

    try:
        q = witness['q']
        P_coeffs = witness['P']
        alpha_coeffs = witness['alpha']
        m_coeffs = witness['m']
        
        P_poly = Poly(P_coeffs, x, domain=GF(q))
        alpha_poly = Poly(alpha_coeffs, x, domain=GF(q))
        m_poly = Poly(m_coeffs, x, domain=GF(q))
        m_list = [int(c) for c in m_poly.all_coeffs()]
        m_list.reverse()
        
        if 'd' in witness:
            d = witness['d']
        else:
            d = m_poly.degree()
            
        S = []
        current = alpha_poly
        for i in range(d):
            S.append(current)
            
            next_elem = Poly(1, x, domain=GF(q))
            base = current
            exp = q
            while exp > 0:
                if exp % 2 == 1:
                    next_elem = next_elem.mul(base).rem(P_poly)
                base = base.mul(base).rem(P_poly)
                exp //= 2
            current = next_elem
            
        S_coeffs = [tuple(int(c) for c in poly.all_coeffs()) for poly in S]
        distinct = len(set(S_coeffs)) == d
        
        all_roots = True
        for poly in S:
            res = Poly(0, x, domain=GF(q))
            alpha_pow = Poly(1, x, domain=GF(q))
            for c in m_list:
                term = alpha_pow.mul(Poly(c, x, domain=GF(q)))
                res = res.add(term).rem(P_poly)
                alpha_pow = alpha_pow.mul(poly).rem(P_poly)
            if not res.is_zero:
                all_roots = False
                break
                
        exactly_roots = distinct and all_roots and (d == m_poly.degree())
        neg_Q = not exactly_roots
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]