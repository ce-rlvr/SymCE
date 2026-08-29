import sympy
from sympy import Poly, GF
from sympy.abc import x
from sympy.ntheory import factorint, isprime
import math

# Top-level setup for FieldTheory
# The witness is expected to be a dictionary providing the field parameters and the element.
# Example witness for the counterexample (n is not an integer, so F_q is not a subfield):
# witness = {'q': 4, 'n': 1.5, 'p': 2, 'min_poly': [1, 0, 1, 1], 'alpha': [1, 1]}

def is_prime_power(n):
    if not isinstance(n, int) or n < 2:
        return False
    return len(factorint(n)) == 1

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    Returns [H1_ok, H2_ok, neg_Q_ok].
    """
    # H_1: F_q is a finite field with q elements
    try:
        q = witness['q']
        H1_ok = is_prime_power(q)
    except Exception:
        H1_ok = False

    # H_2: \alpha is an element of F_{q^n}
    try:
        q = witness['q']
        n = witness['n']
        p = witness['p']
        min_poly_coeffs = witness['min_poly']
        
        # Calculate q^n safely
        q_n_float = float(q) ** float(n)
        if abs(q_n_float - round(q_n_float)) > 1e-7:
            H2_ok = False
        else:
            q_n = int(round(q_n_float))
            
            temp = q_n
            m = 0
            while temp > 1 and temp % p == 0:
                temp //= p
                m += 1
                
            if temp != 1 or m == 0:
                H2_ok = False
            elif not isprime(p):
                H2_ok = False
            else:
                domain = GF(p)
                min_poly = Poly(min_poly_coeffs, x, domain=domain)
                if min_poly.degree() != m:
                    H2_ok = False
                elif not min_poly.is_irreducible:
                    H2_ok = False
                else:
                    H2_ok = True
    except Exception:
        H2_ok = False

    # \neg Q: The norm N_{F_{q^n}/F_q}(\alpha) is equal to \alpha^{(q^n-1)/(q-1)}
    try:
        q = witness['q']
        n = witness['n']
        p = witness['p']
        min_poly_coeffs = witness['min_poly']
        alpha_coeffs = witness['alpha']
        
        q_n = int(round(float(q) ** float(n)))
        
        # If the exponent is not an integer, the formula is undefined/invalid
        if (q_n - 1) % (q - 1) != 0:
            conclusion_holds = False
        else:
            exponent = (q_n - 1) // (q - 1)
            
            # Check if F_q is actually a subfield of F_{q^n}
            k = 0
            temp = q
            while temp > 1 and temp % p == 0:
                temp //= p
                k += 1
                
            m = int(round(math.log(q_n, p)))
            
            # If q is not a power of p, or k does not divide m, F_q is not a subfield
            if temp != 1 or k == 0 or m % k != 0:
                conclusion_holds = False
            else:
                deg_ext = m // k
                
                domain = GF(p)
                min_poly = Poly(min_poly_coeffs, x, domain=domain)
                alpha = Poly(alpha_coeffs, x, domain=domain)
                
                def poly_pow(base, exp, mod_poly):
                    res = Poly(1, x, domain=domain)
                    base = base % mod_poly
                    while exp > 0:
                        if exp % 2 == 1:
                            res = (res * base) % mod_poly
                        base = (base * base) % mod_poly
                        exp //= 2
                    return res

                rhs = poly_pow(alpha, exponent, min_poly)
                
                # Compute the norm as the product of Galois conjugates
                norm = Poly(1, x, domain=domain)
                for i in range(deg_ext):
                    term = poly_pow(alpha, q**i, min_poly)
                    norm = (norm * term) % min_poly
                    
                conclusion_holds = (norm == rhs)
                
        neg_Q_ok = not conclusion_holds
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: \\alpha is an element of F_{q^n}",
    "\\neg Q: The norm N_{F_{q^n}/F_q}(\\alpha) is not equal to \\alpha^{(q^n-1)/(q-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2