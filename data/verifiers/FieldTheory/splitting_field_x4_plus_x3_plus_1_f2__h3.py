import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    h1 = True
    h2 = True
    try:
        if isinstance(witness, int):
            neg_q = (witness != 4 and witness != 16)
        elif hasattr(witness, 'degree'):
            d = witness.degree() if callable(witness.degree) else witness.degree
            neg_q = (d != 4)
        elif hasattr(witness, 'order'):
            o = witness.order() if callable(witness.order) else witness.order
            neg_q = (o != 16)
        else:
            s = str(witness)
            neg_q = (s not in ["4", "16", "GF(16)", "F_16"])
    except Exception:
        neg_q = True
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_2 is the finite field with 2 elements",
    "H_2: f(x) = x^4 + x^3 + 1 in F_2(x)",
    "not Q: The degree of the extension E over F_2 is not 4, or E is not isomorphic to F_16"
]

N_HYP = 2
NEG_Q_INDEX = 2