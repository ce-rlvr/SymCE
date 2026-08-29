import math
from sympy import Poly, Rational, factor_list
from sympy.abc import x
from sympy.ntheory import isprime

def vp(a, p):
    if a == 0:
        return math.inf
    a = Rational(a)
    num, den = a.p, a.q
    
    def count_p(n, p):
        c = 0
        while n % p == 0 and n != 0:
            c += 1
            n //= p
        return c
    
    return count_p(num, p) - count_p(den, p)

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        poly = Poly(f, x, domain='QQ')
        n = poly.degree()
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        if not h1 or not h2:
            h3 = False
        else:
            coeffs = poly.all_coeffs()
            coeffs.reverse()
            a0 = coeffs[0]
            an = coeffs[n]
            
            if a0 == 0 or an == 0:
                h3 = False
            else:
                vp_a0 = vp(a0, p)
                vp_an = vp(an, p)
                
                h3 = True
                for i in range(1, n):
                    ai = coeffs[i]
                    if ai == 0:
                        continue
                    vp_ai = vp(ai, p)
                    if n * vp_ai < n * vp_a0 + i * (vp_an - vp_a0):
                        h3 = False
                        break
    except Exception:
        h3 = False

    try:
        if not h1 or not h2:
            h4 = False
        else:
            coeffs = poly.all_coeffs()
            coeffs.reverse()
            a0 = coeffs[0]
            an = coeffs[n]
            if a0 == 0 or an == 0:
                h4 = False
            else:
                vp_a0 = vp(a0, p)
                vp_an = vp(an, p)
                diff = abs(vp_an - vp_a0)
                h4 = (math.gcd(n, diff) == 1)
    except Exception:
        h4 = False

    try:
        if not h1:
            neg_q = False
        else:
            _, factors = factor_list(poly)
            total_factors = sum(mult for _, mult in factors)
            neg_q = (total_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ['H_1: degree >= 1', 'H_2: p is prime', 'H_3: single segment', 'H_4: gcd is 1', 'not Q: reducible']

N_HYP = 4
NEG_Q_INDEX = 4