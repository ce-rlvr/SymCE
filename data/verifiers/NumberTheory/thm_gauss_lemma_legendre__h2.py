import sympy
import math

# Top-level setup
# No specific named bindings needed for Number Theory witnesses; use integers/rationals directly.

def conditions(witness) -> list[bool]:
    try:
        a, p, n_wit = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False
        
    # H2: \gcd(a, p) = 1
    # If 'a' is a rational number, it is coprime to p if both its numerator and denominator are coprime to p.
    try:
        a_sym = sympy.Rational(a)
        num, den = a_sym.as_numer_denom()
        h2 = bool(sympy.gcd(num, p) == 1 and sympy.gcd(den, p) == 1)
    except Exception:
        try:
            h2 = bool(sympy.gcd(a, p) == 1)
        except Exception:
            h2 = False
            
    # H3: n is the number of integers in the set {a, 2a, ..., ((p-1)/2)a} 
    # whose least positive residue modulo p is strictly greater than p/2
    try:
        a_sym = sympy.Rational(a)
        count = 0
        limit = (p - 1) // 2
        for k in range(1, limit + 1):
            val = k * a_sym
            if val.is_integer:
                # Least positive residue modulo p
                res = int(val) % p
                if res > p / 2:
                    count += 1
        h3 = bool(n_wit == count)
    except Exception:
        h3 = False
        
    # Conclusion: The Legendre symbol (a/p) is equal to (-1)^n
    # We evaluate (a/p) for rational 'a' by taking the modular inverse of the denominator.
    try:
        a_sym = sympy.Rational(a)
        num, den = a_sym.as_numer_denom()
        num = int(num)
        den = int(den)
        inv_den = pow(den, -1, p)
        val_mod_p = (num * inv_den) % p
        leg = sympy.legendre_symbol(val_mod_p, p)
        
        q = (leg == (-1)**n_wit)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: p is an odd prime",
    r"H_2: \gcd(a, p) = 1",
    r"H_3: n is the number of integers in the set \{a, 2a, \dots, \frac{p-1}{2}a\} whose least positive residue modulo p is strictly greater than p/2",
    r"¬Q: The Legendre symbol (a/p) is not equal to (-1)^n"
]

N_HYP = 3
NEG_Q_INDEX = 3