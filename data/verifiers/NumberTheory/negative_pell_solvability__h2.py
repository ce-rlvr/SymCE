import math

CONDITION_LABELS = [
    "H_1: d is a positive integer that is not a perfect square",
    "¬Q: The negative Pell equation x^2 - d y^2 = -1 has integer solutions if and only if m is an odd integer (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            d = int(witness['d'])
            m = int(witness['m']) if 'm' in witness else None
        elif isinstance(witness, (tuple, list)):
            d = int(witness[0])
            m = int(witness[1]) if len(witness) > 1 else None
        else:
            d = int(witness)
            m = None
    except Exception:
        return [False, False]
    
    # H_1: d is a positive integer that is not a perfect square
    try:
        h1 = (d > 0) and (math.isqrt(d)**2 != d)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        a0 = math.isqrt(d)
        if a0 * a0 == d:
            has_sol = False
        else:
            # Compute the period length of the continued fraction of sqrt(d)
            per_len = 0
            p = 0
            q = 1
            a = a0
            seen = {}
            while True:
                p = a * q - p
                q = (d - p * p) // q
                a = (a0 + p) // q
                state = (p, q)
                if state in seen:
                    per_len = per_len - seen[state]
                    break
                seen[state] = per_len
                per_len += 1
            
            # The negative Pell equation has solutions iff the period length is odd
            has_sol = (per_len % 2 == 1)
        
        if m is None:
            # If m is not provided, the statement "has_sol iff m is odd" is treated 
            # as universally quantified over m, which is false for any d.
            q_val = False
        else:
            q_val = (has_sol == (m % 2 == 1))
            
        neg_q = not q_val
    except Exception:
        neg_q = False

    return [h1, neg_q]