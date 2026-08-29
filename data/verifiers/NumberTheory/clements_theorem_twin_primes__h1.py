import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        
        # Prevent DOS from extremely large factorials
        if p > 2000:
            return [False]
            
        # Check if p and p+2 are twin primes
        are_twin_primes = sympy.isprime(p) and sympy.isprime(p + 2)
        
        # Check Clement's congruence: 4((p-1)! + 1) + p == 0 mod p(p+2)
        # math.factorial will raise ValueError for negative numbers, which is caught
        fact = math.factorial(p - 1)
        lhs = 4 * (fact + 1) + p
        modulus = p * (p + 2)
        
        if modulus == 0:
            congruence_holds = (lhs == 0)
        else:
            congruence_holds = (lhs % modulus == 0)
            
        # The conclusion is an equivalence (iff). It fails if the two sides have different truth values.
        neg_q = bool(are_twin_primes != congruence_holds)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence between p, p+2 being twin primes and Clement's congruence fails"
]

N_HYP = 0
NEG_Q_INDEX = 0