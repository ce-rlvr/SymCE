import sympy
import math
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p', 2)
            f_coeffs = witness.get('f_coeffs', [0])
            f_prime_coeffs = witness.get('f_prime_coeffs', f_coeffs)
            d = witness.get('E_degree', 1)
            d_prime = witness.get('E_prime_degree', 2)
        else:
            p = getattr(witness, 'p', 2)
            f_coeffs = getattr(witness, 'f_coeffs', [0])
            f_prime_coeffs = getattr(witness, 'f_prime_coeffs', f_coeffs)
            d = getattr(witness, 'E_degree', 1)
            d_prime = getattr(witness, 'E_prime_degree', 2)
            
        def lcm(a, b):
            return abs(a * b) // math.gcd(a, b) if a and b else 0

        try:
            h1 = sympy.isprime(p)
        except Exception:
            h1 = False
            
        try:
            is_list = isinstance(f_coeffs, list)
            h2 = is_list and all(isinstance(c, int) for c in f_coeffs)
        except Exception:
            h2 = False
            
        try:
            is_list_p = isinstance(f_prime_coeffs, list)
            h3 = is_list_p and (f_coeffs == f_prime_coeffs)
        except Exception:
            h3 = False
            
        try:
            if not sympy.isprime(p):
                h4 = False
            else:
                f_expr = sum(c * x**i for i, c in enumerate(f_coeffs))
                f = sympy.Poly(f_expr, x, domain=sympy.GF(p))
                if f.is_zero:
                    h4 = (isinstance(d, int) and d >= 1)
                else:
                    factors = sympy.factor_list(f)[1]
                    degrees = [fac[0].degree() for fac in factors]
                    k = 1
                    for deg in degrees:
                        k = lcm(k, deg)
                    h4 = (d == k)
        except Exception:
            h4 = False
            
        try:
            if not sympy.isprime(p):
                h5 = False
            else:
                f_p_expr = sum(c * x**i for i, c in enumerate(f_prime_coeffs))
                f_p = sympy.Poly(f_p_expr, x, domain=sympy.GF(p))
                if f_p.is_zero:
                    h5 = (isinstance(d_prime, int) and d_prime >= 1)
                else:
                    factors_p = sympy.factor_list(f_p)[1]
                    degrees_p = [fac[0].degree() for fac in factors_p]
                    k_p = 1
                    for deg in degrees_p:
                        k_p = lcm(k_p, deg)
                    h5 = (d_prime == k_p)
        except Exception:
            h5 = False
            
        try:
            neg_q = (d != d_prime)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]
    except Exception:
        return [False] * 6

CONDITION_LABELS = [
    "H_1: phi is an isomorphism",
    "H_2: f is a polynomial",
    "H_3: f_prime is the image of f",
    "H_4: E is a splitting field of f",
    "H_5: E_prime is a splitting field of f_prime",
    "neg_Q: tau does not exist"
]

N_HYP = 5
NEG_Q_INDEX = 5