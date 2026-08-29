import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

def conditions(witness):
    # H_1: F is a field
    try:
        h1_ok = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1_ok = False

    # ¬Q: F is perfect iff the Frobenius endomorphism is surjective is FALSE
    try:
        c = None
        if hasattr(witness, 'char'):
            c = witness.char
            if callable(c):
                c = c()
        elif hasattr(witness, 'characteristic'):
            c = witness.characteristic
            if callable(c):
                c = c()
        
        if c == 0:
            # For characteristic 0, F is always perfect, but the Frobenius 
            # endomorphism x \mapsto x^p is undefined (or not surjective if p=0 is attempted).
            # Thus, the equivalence (True iff False) fails.
            neg_q_ok = True
        elif c is not None and c > 0:
            # For characteristic p > 0, the equivalence holds.
            neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: F is perfect iff the Frobenius endomorphism is surjective is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1