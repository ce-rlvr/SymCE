import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Named object bindings
# No specific named bindings needed for RingTheory beyond ZZ, QQ, x

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a = u p_1^{k_1} \cdots p_m^{k_m} is a factorization of a, where p_i are prime elements, k_i are positive integers, and u is a unit",
    "¬Q: The R-module R/<a> does not have finite length equal to \sum_{i=1}^m k_i"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            a = witness.get('a')
            u = witness.get('u')
            p = witness.get('p', [])
            k = witness.get('k', [])
        else:
            R, a, u, p, k = witness
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain
    try:
        h1 = False
        if R == ZZ:
            h1 = True
        elif getattr(R, 'is_PID', False):
            h1 = True
    except Exception:
        h1 = False

    # H2: a = u p_1^{k_1} \cdots p_m^{k_m} is a factorization of a, where p_i are prime elements, k_i are positive integers, and u is a unit
    try:
        h2 = True
        
        # Check if u is a unit
        if R == ZZ:
            if u not in [1, -1]:
                h2 = False
        elif hasattr(R, 'is_unit'):
            if not R.is_unit(u):
                h2 = False
        else:
            if u not in [1, -1]:
                h2 = False
        
        # Check if k_i are positive integers
        if any(not (isinstance(ki, (int, sympy.Integer)) and ki > 0) for ki in k):
            h2 = False
            
        # Check if p_i are prime elements
        from sympy import isprime
        for pi in p:
            is_prime_el = False
            if pi == 0:
                # In an integral domain, the zero ideal is prime, so 0 is a prime element.
                # This is the crux of the counterexample when the "a != 0" hypothesis is dropped.
                is_prime_el = True
            elif R == ZZ:
                try:
                    is_prime_el = isprime(abs(int(pi)))
                except Exception:
                    is_prime_el = False
            elif hasattr(R, 'is_prime'):
                is_prime_el = R.is_prime(pi)
            else:
                try:
                    is_prime_el = isprime(abs(int(pi)))
                except Exception:
                    is_prime_el = False
                    
            if not is_prime_el:
                h2 = False
                break
                
        # Check if the product equals a
        prod = u
        for pi, ki in zip(p, k):
            prod = prod * (pi ** ki)
            
        if prod != a:
            try:
                if sympy.simplify(prod - a) != 0:
                    h2 = False
            except Exception:
                h2 = False
                
    except Exception:
        h2 = False

    # neg_Q: The R-module R/<a> does not have finite length equal to \sum_{i=1}^m k_i
    try:
        if a == 0:
            if getattr(R, 'is_Field', False):
                length = 1
                neg_q = (length != sum(k))
            else:
                # For a PID that is not a field, R/<0> = R has infinite length
                neg_q = True 
        else:
            # For a != 0, the length is exactly the number of prime factors (sum of k_i)
            length = sum(k)
            neg_q = (length != sum(k)) # This will be False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]