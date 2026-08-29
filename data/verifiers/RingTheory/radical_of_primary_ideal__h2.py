import sympy
from sympy import isprime, ZZ, QQ
from sympy.ntheory import factorint
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # Try to parse witness as an integer representing the generator of an ideal in ZZ
        if isinstance(witness, tuple) and len(witness) == 2:
            # Could be (Ring, Ideal)
            ring, ideal = witness
            if isinstance(ideal, (list, tuple, set)):
                n = int(list(ideal)[0])
            else:
                n = int(ideal)
        elif isinstance(witness, (list, tuple, set)):
            n = int(list(witness)[0])
        else:
            n = int(witness)
            
        # H_1: R is a commutative ring
        # Since we are evaluating the witness in ZZ, this is always True.
        h1 = True
        
        # neg_Q: The radical of Q is NOT a prime ideal
        if n == 0:
            rad_n = 0
        else:
            factors = factorint(abs(n))
            rad_n = 1
            for p in factors:
                rad_n *= p
                
        # In ZZ, an ideal kZZ is prime iff k == 0 or k is a prime number.
        # Note: k=1 gives ZZ, which is not a proper ideal, hence not prime.
        is_prime_ideal = (rad_n == 0) or isprime(rad_n)
        
        neg_q = not is_prime_ideal
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The radical of Q is not a prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1