import sympy
import math

# Top-level setup
# (No specific named objects required for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    def is_valid_int(x):
        if isinstance(x, bool):
            return False
        if isinstance(x, int):
            return True
        if isinstance(x, float):
            return x.is_integer()
        if hasattr(x, 'is_integer'):
            prop = getattr(x, 'is_integer')
            if callable(prop):
                return prop()
            return bool(prop)
        return False

    try:
        n_raw, p_raw = witness
        if not (is_valid_int(n_raw) and is_valid_int(p_raw)):
            return [False, False, False, False]
        n = int(n_raw)
        p = int(p_raw)
    except Exception:
        return [False, False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = (n > 0)
    except Exception:
        h1 = False
        
    # H_2: p is a prime
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H_3: p divides F_n
    try:
        if n < 0:
            h3 = False
        elif p == 0:
            h3 = False
        else:
            abs_p = abs(p)
            if abs_p == 1:
                h3 = True
            elif abs_p == 2:
                h3 = False
            else:
                if sympy.isprime(abs_p):
                    phi = abs_p - 1
                    exp = pow(2, n, phi)
                    h3 = (pow(2, exp, abs_p) == abs_p - 1)
                else:
                    if n <= 10**6:
                        # O(n) squarings, extremely fast for n up to 1,000,000
                        h3 = (pow(2, 1 << n, abs_p) == abs_p - 1)
                    else:
                        # n is huge, p is composite. Use totient if p is small enough to factor quickly.
                        if abs_p <= 10**6:
                            phi = sympy.totient(abs_p)
                            exp = pow(2, n, phi)
                            h3 = (pow(2, exp, abs_p) == abs_p - 1)
                        else:
                            # Prevent TLE for maliciously huge n and huge composite p
                            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: p ≡ 1 (mod 2^{n+1}) fails
    try:
        if n < -1:
            neg_q = False
        else:
            if n >= p.bit_length() + 1:
                if p >= 0:
                    neg_q = (p != 1)
                else:
                    neg_q = True
            else:
                mod = 1 << (n + 1)
                neg_q = (p % mod != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime",
    "H_3: p divides F_n",
    "¬Q: p is not 1 (mod 2^{n+1})"
]

N_HYP = 3
NEG_Q_INDEX = 3