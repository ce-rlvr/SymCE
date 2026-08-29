import sympy
import math

def conditions(witness):
    try:
        # Ensure witness is an integer-like object
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        p = int(witness)
        
        if p == 0:
            q = False
        else:
            # The modular inverse exists iff gcd(p-2, p) == 1
            if math.gcd(p - 2, p) != 1:
                q = False
            # (p-1)/2 must be an integer for the congruence to make sense
            elif (p - 1) % 2 != 0:
                q = False
            else:
                inv = pow(p - 2, -1, abs(p))
                expected = (p - 1) // 2
                q = (inv % abs(p)) == (expected % abs(p))
                
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of p - 2 modulo p is not congruent to (p-1)/2 mod p (or does not exist)"
]

N_HYP = 0
NEG_Q_INDEX = 0