import sympy

def conditions(witness):
    try:
        # Extract the ideal generator if a tuple/list is provided (e.g., (ZZ, 0))
        if isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                witness = witness[1]
            elif len(witness) == 1:
                witness = witness[0]
        
        n = int(witness)
        if float(witness) != n:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a principal ideal domain
    # We evaluate this in Z, which is always a PID.
    try:
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: I is a proper ideal of R
    # In Z, the ideal (n) is proper iff n != 1 and n != -1
    try:
        h2_ok = abs(n) != 1
    except Exception:
        h2_ok = False
        
    # ¬Q: I cannot be uniquely factored into a product of prime ideals
    # In Z, (n) is uniquely factored iff n != 0 (for proper ideals).
    # If n == 0, (0) = (0)*(2) = (0)*(3) = (0)*(0), so factorization is not unique.
    try:
        neg_q_ok = (n == 0)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: I is a proper ideal of R",
    "¬Q: I cannot be uniquely factored into a product of prime ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2