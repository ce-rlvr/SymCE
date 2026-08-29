import math

def conditions(witness):
    # H_1: Let m = n + 2
    try:
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('N'))
            m = witness.get('m', witness.get('M'))
        elif isinstance(witness, (tuple, list)):
            n, m = witness
        else:
            n = witness
            m = n + 2
        
        n = int(n)
        m = int(m)
        h1 = (m == n + 2)
    except Exception:
        h1 = False

    # ¬Q: The modular inverse of n modulo m is not congruent to (n+1)/2 (mod m)
    try:
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('N'))
            m = witness.get('m', witness.get('M'))
        elif isinstance(witness, (tuple, list)):
            n, m = witness
        else:
            n = witness
            m = n + 2
            
        n = int(n)
        m = int(m)
        
        if m == 0:
            # Modulo 0 is undefined, so the conclusion fails
            neg_q = True
        else:
            if math.gcd(n, m) != 1:
                # Modular inverse does not exist, so the conclusion fails
                neg_q = True
            elif abs(m) == 1:
                # Modulo 1, all integers are congruent, so the conclusion holds
                neg_q = False
            else:
                if (n + 1) % 2 != 0:
                    # (n+1)/2 is not an integer, so it cannot be congruent to the inverse
                    neg_q = True
                else:
                    inv = pow(n % abs(m), -1, abs(m))
                    val = (n + 1) // 2
                    if (inv - val) % abs(m) == 0:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let m = n + 2",
    "¬Q: The modular inverse of n modulo m is not congruent to (n+1)/2 (mod m)"
]

N_HYP = 1
NEG_Q_INDEX = 1