import sympy
from sympy import abc

# Top-level setup
x = sympy.Symbol('x')

def vp(a, p):
    if a == 0:
        return float('inf')
    a = sympy.Rational(a)
    num = a.p
    den = a.q
    m_num = sympy.multiplicity(p, num)
    m_den = sympy.multiplicity(p, den)
    if m_num is None: m_num = 0
    if m_den is None: m_den = 0
    return m_num - m_den

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: f(x) is a polynomial over Q of degree n >= 1
    try:
        if hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
            sym = list(f.free_symbols)[0]
        else:
            sym = x
        f_poly = sympy.Poly(f, sym, domain='QQ')
        n = f_poly.degree()
        h1 = bool(n >= 1)
    except Exception:
        h1 = False

    # H2: a_0 != 0
    try:
        if h1:
            a0 = f_poly.nth(0)
            h2 = bool(a0 != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(sympy.isprime(p))
    except Exception:
        h3 = False

    # H4: The p-adic Newton polygon of f(x) consists of a single line segment connecting (0, v_p(a_0)) and (n, v_p(a_n))
    try:
        if not (h1 and h2 and h3):
            h4 = False
        else:
            coeffs = f_poly.all_coeffs()
            coeffs.reverse()
            a0 = coeffs[0]
            an = coeffs[n]
            v0 = vp(a0, p)
            vn = vp(an, p)
            h4 = True
            for i in range(1, n):
                ai = coeffs[i]
                if ai != 0:
                    vi = vp(ai, p)
                    # Check if the point (i, vi) is on or above the line segment
                    # Equivalently: vi >= v0 + i * (vn - v0) / n
                    if n * vi < n * v0 + i * (vn - v0):
                        h4 = False
                        break
    except Exception:
        h4 = False

    # neg_Q: f(x) is reducible over Q
    try:
        if not h1:
            neg_q = False
        else:
            factors = sympy.factor_list(f_poly)[1]
            # Count the number of irreducible factors of degree >= 1 (with multiplicity)
            num_factors = sum(mult for factor, mult in factors if factor.degree() >= 1)
            neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q of degree n >= 1",
    "H_2: a_0 != 0",
    "H_3: p is a prime number",
    "H_4: The p-adic Newton polygon of f(x) consists of a single line segment connecting (0, v_p(a_0)) and (n, v_p(a_n))",
    "not Q: f(x) is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4