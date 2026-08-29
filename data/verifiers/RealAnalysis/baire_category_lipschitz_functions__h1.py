import sympy

def conditions(witness):
    try:
        if isinstance(witness, sympy.Interval):
            a = witness.start
            b = witness.end
            neg_q = bool(a >= b)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, b = witness
            neg_q = bool(a >= b)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: The set of Lipschitz functions on the interval is not meager"]

N_HYP = 0
NEG_Q_INDEX = 0