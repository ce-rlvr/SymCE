import sympy
from sympy import isprime, totient

# Top-level setup
# (No specific named objects needed for this number theory problem)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to provide values for n, p, and k.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            k = witness.get('k')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 3:
            n = witness[0]
            p = witness[1]
            k = witness[2]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let n be a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: Let p be a prime number that divides n
    try:
        h2 = isinstance(p, (int, sympy.Integer)) and isprime(p) and (n % p == 0)
    except Exception:
        h2 = False

    # ¬Q: The ramification index of any prime ideal lying over p in Q(zeta_n) is NOT exactly phi(p^k)
    try:
        if not isinstance(k, (int, sympy.Integer)) or k < 0:
            neg_q = False
        else:
            # The true ramification index of p in Q(zeta_n) is phi(p^v), 
            # where v is the exact power of p dividing n.
            v = 0
            temp = n
            while temp > 0 and temp % p == 0:
                v += 1
                temp //= p
            
            actual_ramification_index = totient(p**v)
            claimed_ramification_index = totient(p**k)
            
            neg_q = bool(actual_ramification_index != claimed_ramification_index)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number that divides n",
    "¬Q: The ramification index of p in Q(zeta_n) is not exactly phi(p^k)"
]

N_HYP = 2
NEG_Q_INDEX = 2