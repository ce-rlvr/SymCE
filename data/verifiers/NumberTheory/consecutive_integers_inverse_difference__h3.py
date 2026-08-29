import math

def conditions(witness):
    try:
        n, a = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val > 1)
    except Exception:
        h1 = False
        n_val = 1
        
    try:
        a_val = int(a)
        h2 = (a_val == a)
    except Exception:
        h2 = False
        a_val = 0
        
    try:
        h3 = math.gcd(a_val + 1, n_val) == 1
    except Exception:
        h3 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            try:
                inv_a = pow(a_val, -1, n_val)
                inv_a1 = pow(a_val + 1, -1, n_val)
                inv_aa1 = pow(a_val * (a_val + 1), -1, n_val)
                neg_q = (inv_aa1 % n_val) != ((inv_a - inv_a1) % n_val)
            except ValueError:
                # If any required modular inverse does not exist, the conclusion fails.
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer",
    "H_3: \\gcd(a+1, n) = 1",
    "¬Q: The modular inverse of a(a+1) mod n is not congruent to a^{-1} - (a+1)^{-1} mod n (or an inverse does not exist)"
]

N_HYP = 3
NEG_Q_INDEX = 3