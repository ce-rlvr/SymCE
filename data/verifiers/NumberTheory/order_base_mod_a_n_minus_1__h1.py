import math

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, n).
    """
    try:
        a, n = witness
    except Exception:
        return [False, False]
    
    # H_1: n is a positive integer (and a is an integer, as implied by the domain)
    try:
        h1 = type(n) is int and n > 0 and type(a) is int
    except Exception:
        h1 = False
        
    # ¬Q: The multiplicative order of a modulo a^n - 1 is NOT exactly n.
    try:
        m = a**n - 1
        m_abs = abs(m)
        
        if m_abs == 1:
            order = 1
        elif m_abs == 0:
            if a == 1: 
                order = 1
            elif a == -1: 
                order = 2
            else: 
                order = float('inf')
        else:
            if math.gcd(a, m_abs) != 1:
                order = float('inf')
            else:
                # The order must divide n, so we only check divisors of n
                divisors = []
                for i in range(1, int(n**0.5) + 1):
                    if n % i == 0:
                        divisors.append(i)
                        if i * i != n:
                            divisors.append(n // i)
                divisors.sort()
                
                order = float('inf')
                for d in divisors:
                    if pow(a, d, m_abs) == 1:
                        order = d
                        break
                        
        neg_q = (order != n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The multiplicative order of a modulo a^n - 1 is not exactly n"
]

N_HYP = 1
NEG_Q_INDEX = 1