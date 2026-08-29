import sympy
from sympy import QQ, ZZ, GF

F2 = GF(2)
F3 = GF(3)
F5 = GF(5)

def conditions(witness) -> list[bool]:
    h1 = False
    char = None
    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
            char = witness.characteristic()
        elif isinstance(witness, (int, sympy.Integer)):
            if witness == 0 or sympy.isprime(witness):
                h1 = True
                char = int(witness)
    except Exception:
        pass

    neg_q = False
    try:
        if h1 and char == 2:
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: Factor ring not isomorphic to subring"]
N_HYP = 1
NEG_Q_INDEX = 1