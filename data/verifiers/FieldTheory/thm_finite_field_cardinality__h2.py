import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC, GF
from sympy.ntheory import factorint

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'order'):
            try:
                order = int(witness.order)
                factors = factorint(order)
                if len(factors) == 1 and list(factors.values())[0] >= 1:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                # E.g. if order is infinite and int() fails
                neg_q = True
        else:
            # If it doesn't have an order, it's typically an infinite field like QQ
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The number of elements in F is not p^n for any prime p and positive integer n"
]

N_HYP = 1
NEG_Q_INDEX = 1