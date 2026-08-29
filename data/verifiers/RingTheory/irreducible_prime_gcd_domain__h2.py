import sympy
from sympy import isprime
from sympy.abc import x, y, z

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        # The witness can be a tuple (domain, p) or just the element p.
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, p = witness
        else:
            p = witness

        # Exclude booleans and floats which might otherwise bypass type checks
        if isinstance(p, bool) or isinstance(p, float):
            return [False, False]

        # Case 1: p is an integer (implies domain is ZZ, which is a GCD domain)
        if isinstance(p, (int, sympy.Integer)):
            h1_ok = True
            val = abs(int(p))
            is_prime_elem = isprime(val)
            neg_q_ok = not is_prime_elem
            
        # Case 2: p is a sympy Poly (implies domain is a polynomial ring, which is a GCD domain)
        elif isinstance(p, sympy.Poly):
            h1_ok = True
            is_prime_elem = p.is_irreducible
            if is_prime_elem is None:
                return [False, False]
            neg_q_ok = not is_prime_elem
            
        # Case 3: p is a sympy Expr (convertible to Poly)
        elif isinstance(p, sympy.Expr):
            poly = sympy.Poly(p)
            h1_ok = True
            is_prime_elem = poly.is_irreducible
            if is_prime_elem is None:
                return [False, False]
            neg_q_ok = not is_prime_elem

    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a greatest common divisor (GCD) domain",
    "¬Q: The element p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1