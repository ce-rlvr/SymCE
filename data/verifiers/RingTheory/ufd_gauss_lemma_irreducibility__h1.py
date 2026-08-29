import sympy as sp
from sympy import Poly
from sympy.abc import x
import math
from fractions import Fraction
from functools import reduce
from sympy.ntheory import factorint

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: f is a primitive polynomial over R of positive degree",
    "H_3: f is irreducible over R",
    "not Q: f is reducible over F"
]

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False] * 4
            
        d, f = witness
        
        h1 = False
        if isinstance(d, int) and d != 0 and d != 1:
            factors = factorint(abs(d))
            if all(v == 1 for v in factors.values()):
                h1 = True
                
        p = Poly(f, x)
        deg = p.degree()
        h2 = False
        if deg > 0:
            coeffs = p.coeffs()
            if all(c.is_Integer for c in coeffs):
                g = reduce(math.gcd, [abs(int(c)) for c in coeffs])
                if g == 1:
                    h2 = True
                    
        h3 = False
        neg_q = False
        
        if deg == 2 and h1 and h2:
            a, b, c = [int(coeff) for coeff in p.coeffs()]
            disc = b**2 - 4*a*c
            
            is_sq_Q = False
            if disc >= 0:
                s = math.isqrt(disc)
                if s*s == disc:
                    is_sq_Q = True
                    
            is_sq_d = False
            if d != 0 and disc * d > 0:
                sd = math.isqrt(disc * d)
                if sd * sd == disc * d:
                    is_sq_d = True
                    
            if is_sq_Q or is_sq_d:
                neg_q = True
            else:
                neg_q = False
                
            if not neg_q:
                h3 = True
            else:
                divisors_of_a = []
                if d < 0:
                    max_u = math.isqrt(a**2)
                    for u in range(-max_u, max_u + 1):
                        max_v = math.isqrt(a**2 // abs(d)) if d != 0 else 0
                        for v in range(-max_v, max_v + 1):
                            if u == 0 and v == 0:
                                continue
                            normA = u**2 - d * v**2
                            if normA != 0 and (a**2) % normA == 0:
                                if (a * u) % normA == 0 and (a * v) % normA == 0:
                                    divisors_of_a.append((u, v))
                else:
                    for u in range(-abs(a)*20, abs(a)*20 + 1):
                        for v in range(-abs(a)*20, abs(a)*20 + 1):
                            if u == 0 and v == 0:
                                continue
                            normA = u**2 - d * v**2
                            if normA != 0 and (a**2) % normA == 0:
                                if (a * u) % normA == 0 and (a * v) % normA == 0:
                                    divisors_of_a.append((u, v))
                                    
                if is_sq_Q:
                    s = math.isqrt(disc)
                    r1_p = Fraction(-b + s, 2*a)
                    r1_q = Fraction(0)
                    r2_p = Fraction(-b - s, 2*a)
                    r2_q = Fraction(0)
                elif is_sq_d:
                    sd = math.isqrt(disc * d)
                    r1_p = Fraction(-b, 2*a)
                    r1_q = Fraction(sd, 2*a*d)
                    r2_p = Fraction(-b, 2*a)
                    r2_q = Fraction(-sd, 2*a*d)
                else:
                    r1_p = r1_q = r2_p = r2_q = Fraction(0)
                    
                h3 = True
                for u1, v1 in divisors_of_a:
                    normA = u1**2 - d * v1**2
                    u2 = (a * u1) // normA
                    v2 = (-a * v1) // normA
                    
                    B_p = u1 * r1_p + v1 * r1_q * d
                    B_q = u1 * r1_q + v1 * r1_p
                    
                    D_p = u2 * r2_p + v2 * r2_q * d
                    D_q = u2 * r2_q + v2 * r2_p
                    
                    if B_p.denominator == 1 and B_q.denominator == 1 and D_p.denominator == 1 and D_q.denominator == 1:
                        h3 = False
                        break
                        
                    B_p = u1 * r2_p + v1 * r2_q * d
                    B_q = u1 * r2_q + v1 * r2_p
                    
                    D_p = u2 * r1_p + v2 * r1_q * d
                    D_q = u2 * r1_q + v2 * r1_p
                    
                    if B_p.denominator == 1 and B_q.denominator == 1 and D_p.denominator == 1 and D_q.denominator == 1:
                        h3 = False
                        break

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False] * 4