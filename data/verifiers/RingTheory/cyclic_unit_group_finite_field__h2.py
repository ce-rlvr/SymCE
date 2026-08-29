import sympy
from sympy import isprime, reduced_totient, totient

# Top-level setup
# We represent finite rings Z/nZ as integers n.
# A tuple (p, k) can represent the finite field GF(p^k).
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # If witness is an integer n, it represents the ring Z/nZ
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n > 1:
                # Z/nZ is a finite field if and only if n is prime
                h1 = isprime(n)
                
                # The group of units (Z/nZ)^x has order totient(n).
                # It is a cyclic group if and only if the Carmichael function (reduced_totient)
                # equals the Euler totient function.
                is_cyclic = (reduced_totient(n) == totient(n))
                neg_q = not is_cyclic
                
        # If witness is a tuple (p, k), it represents the finite field GF(p^k)
        elif isinstance(witness, tuple) and len(witness) == 2:
            p, k = witness
            if isinstance(p, (int, sympy.Integer)) and isinstance(k, (int, sympy.Integer)):
                p, k = int(p), int(k)
                if p > 1 and k >= 1:
                    # It is a valid finite field if p is prime
                    h1 = isprime(p)
                    
                    # The multiplicative group of any finite field GF(p^k) is always cyclic.
                    # Therefore, the conclusion never fails for a valid finite field.
                    neg_q = False
                    
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: F^{\\times} is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1