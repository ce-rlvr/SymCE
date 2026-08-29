import sympy
import math

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: k is an integer
    try:
        h2 = (int(k) == k)
    except Exception:
        h2 = False
        
    # neg_Q: The modular inverse of k! modulo p is NOT congruent to (-1)^{k+1} * (p - 1 - k)! (mod p)
    try:
        k_int = int(k)
        p_int = int(p)
        
        # If factorials would be undefined, the conclusion formula is invalid (hence fails)
        if k_int < 0 or p_int - 1 - k_int < 0:
            q_ok = False
        else:
            fact_k = math.factorial(k_int)
            # If k! is not invertible modulo p, the conclusion fails
            if math.gcd(fact_k, p_int) != 1:
                q_ok = False
            else:
                inv_fact_k = pow(fact_k, -1, p_int)
                rhs = ((-1)**(k_int + 1) * math.factorial(p_int - 1 - k_int)) % p_int
                q_ok = (inv_fact_k == rhs)
    except Exception:
        q_ok = False
        
    neg_q = not q_ok
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is an integer",
    "¬Q: The modular inverse of k! modulo p is not congruent to (-1)^{k+1} * (p - 1 - k)! (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2