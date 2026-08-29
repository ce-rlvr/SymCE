import sympy

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, int) and not isinstance(witness, bool):
            n = witness
            if n >= 2:
                h1 = True
                idemps = [i for i in range(n) if (i * i) % n == i]
                if len(idemps) > 2:
                    neg_q = True
        elif isinstance(witness, tuple) and len(witness) > 0:
            if all(isinstance(w, int) and not isinstance(w, bool) and w >= 2 for w in witness):
                h1 = True
                if len(witness) >= 2:
                    neg_q = True
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "not Q: The polynomial ring has idempotent elements other than 0 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1