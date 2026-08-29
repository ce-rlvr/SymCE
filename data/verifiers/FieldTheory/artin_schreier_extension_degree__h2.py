import sympy
from sympy import Poly, GF, isprime
from sympy.abc import x
import math

def get_lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    """
    witness: tuple (p, d, a_val)
    where:
      p is a prime (characteristic of K)
      d is the degree of K over GF(p), so K = GF(p^d)
      a_val is the minimal polynomial of 'a' over GF(p) (as a sympy Expr, Poly, or list of coeffs)
      or an integer if 'a' is in GF(p).
      (e.g., witness = (2, 1, x**2 + x + 1) for K=GF(2) and a in GF(4) with a^2+a+1=0)
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        p, d, a_val = witness
        
        if hasattr(p, 'is_Integer') and p.is_Integer:
            p = int(p)
        if hasattr(d, 'is_Integer') and d.is_Integer:
            d = int(d)
            
        if not isprime(p):
            return [False, False, False]
        if not isinstance(d, int) or d < 1:
            return [False, False, False]
            
        if isinstance(a_val, int) or (hasattr(a_val, 'is_Integer') and a_val.is_Integer):
            a_val = x - a_val
            
        poly = Poly(a_val, x, domain=GF(p))
        a_coeffs = [int(c % p) for c in poly.all_coeffs()]
        
        if len(a_coeffs) < 2:
            return [False, False, False]
            
        if a_coeffs[0] != 1:
            inv = pow(a_coeffs[0], p - 2, p)
            a_coeffs = [(c * inv) % p for c in a_coeffs]
            poly = Poly(a_coeffs, x, domain=GF(p))
            
        if not poly.is_irreducible:
            return [False, False, False]
            
        k = len(a_coeffs) - 1
        
        # H1: K is a field of characteristic p > 0
        h1 = True
        
        # H2: The polynomial x^p - x - a has no roots in K
        if d % k != 0:
            h2 = True
        else:
            tr_a_GFpk = (-a_coeffs[1]) % p
            tr_a_K = ((d // k) * tr_a_GFpk) % p
            h2 = (tr_a_K != 0)
            
        # Conclusion: The splitting field of x^p - x - a over K has degree p over K
        tr_a_GFpk = (-a_coeffs[1]) % p
        if tr_a_GFpk == 0:
            m_r = k
        else:
            m_r = k * p
            
        m = get_lcm(d, m_r)
        deg_over_K = m // d
        
        neg_q = (deg_over_K != p)
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic p > 0",
    "H_2: The polynomial x^p - x - a has no roots in K",
    "¬Q: The splitting field of x^p - x - a over K does not have degree p over K"
]

N_HYP = 2
NEG_Q_INDEX = 2