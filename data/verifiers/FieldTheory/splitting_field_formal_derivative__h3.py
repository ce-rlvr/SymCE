import sympy
from sympy import Poly, QQ, isprime
from sympy.abc import x
import math

# Top-level setup for witness evaluation
# We provide QQ and x for standard field theory witnesses.
# A witness can be a tuple (F, f, K, L) using SymPy objects,
# or a tuple (p, f_coeffs, k, m) for finite fields GF(p).

def conditions(witness):
    h1 = h2 = h3 = neg_q = False
    
    try:
        # Check if witness is finite field dict
        if isinstance(witness, dict) and 'p' in witness:
            p = int(witness['p'])
            f_coeffs = [int(c) for c in witness['f_coeffs']]
            k = int(witness['k'])
            m = int(witness['m'])
            
            # H1: F is a field
            h1 = isprime(p)
            
            # H2: f in F[x] is non-constant
            coeffs = list(f_coeffs)
            while coeffs and coeffs[0] % p == 0:
                coeffs.pop(0)
            h2 = len(coeffs) > 1
            
            # H3: L is splitting field of f' over F
            if h1 and h2:
                f = Poly.from_list(coeffs, gens=x, domain=sympy.GF(p))
                f_prime = f.diff(x)
                if f_prime.is_zero:
                    h3 = (m == 1)
                else:
                    factors = f_prime.factor_list()[1]
                    degrees = [factor.degree() for factor, exp in factors]
                    lcm = 1
                    for d in degrees:
                        lcm = (lcm * d) // math.gcd(lcm, d)
                    h3 = (m == lcm)
            
            # neg_Q: L is not a subfield of K
            neg_q = (k % m != 0)
            
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
            
        # Check if witness is finite field tuple
        elif isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], (int, sympy.Integer)):
            p = int(witness[0])
            f_coeffs = [int(c) for c in witness[1]]
            k = int(witness[2])
            m = int(witness[3])
            
            h1 = isprime(p)
            
            coeffs = list(f_coeffs)
            while coeffs and coeffs[0] % p == 0:
                coeffs.pop(0)
            h2 = len(coeffs) > 1
            
            if h1 and h2:
                f = Poly.from_list(coeffs, gens=x, domain=sympy.GF(p))
                f_prime = f.diff(x)
                if f_prime.is_zero:
                    h3 = (m == 1)
                else:
                    factors = f_prime.factor_list()[1]
                    degrees = [factor.degree() for factor, exp in factors]
                    lcm = 1
                    for d in degrees:
                        lcm = (lcm * d) // math.gcd(lcm, d)
                    h3 = (m == lcm)
                    
            neg_q = (k % m != 0)
            
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
            
        # Otherwise, assume witness is (F, f, K, L) with F = QQ
        elif isinstance(witness, tuple) and len(witness) == 4:
            F, f_poly, K, L = witness
            
            # H1: F is a field
            h1 = (F == QQ)
            
            # H2: f in F[x] is non-constant
            try:
                if not isinstance(f_poly, Poly):
                    f_poly = Poly(f_poly, x, domain=F)
                h2 = f_poly.degree() > 0 and f_poly.domain == F
            except Exception:
                h2 = False
                
            # H3: L is splitting field of f' over F
            try:
                if h1 and h2:
                    f_prime = f_poly.diff()
                    if f_prime.is_zero:
                        h3 = (L == F)
                    else:
                        factors = Poly(f_prime, domain=L).factor_list()[1]
                        splits_completely = all(fac.degree() == 1 for fac, exp in factors)
                        
                        roots = sympy.roots(f_prime)
                        if sum(roots.values()) == f_prime.degree():
                            irr_roots = [r for r in roots.keys() if not r.is_Rational]
                            if irr_roots:
                                expected_L = QQ.algebraic_field(*irr_roots)
                                deg_expected = expected_L.ext.minpoly.degree() if hasattr(expected_L, 'ext') else 1
                            else:
                                deg_expected = 1
                                
                            deg_L = L.ext.minpoly.degree() if hasattr(L, 'ext') else 1
                            is_minimal = (deg_L == deg_expected)
                        else:
                            is_minimal = True
                            
                        h3 = splits_completely and is_minimal
            except Exception:
                h3 = False
                
            # neg_Q: L is not a subfield of K
            try:
                if L == QQ:
                    neg_q = False
                elif K == QQ:
                    neg_q = True
                else:
                    minpoly_L = L.ext.minpoly
                    factors_in_K = Poly(minpoly_L, domain=K).factor_list()[1]
                    has_root_in_K = any(fac.degree() == 1 for fac, exp in factors_in_K)
                    neg_q = not has_root_in_K
            except Exception:
                neg_q = False
                
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
            
    except Exception:
        pass
        
    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "H_3: L is the splitting field of the formal derivative of f over F",
    "neg_Q: L is not a subfield of K"
]

N_HYP = 3
NEG_Q_INDEX = 3