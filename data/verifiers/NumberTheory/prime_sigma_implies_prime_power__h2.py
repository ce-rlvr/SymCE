import sympy

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            h1 = False
        else:
            h1 = bool(witness > 0)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            neg_q = False
        else:
            n = int(witness)
            if n <= 1:
                neg_q = True
            else:
                factors = sympy.factorint(n)
                neg_q = bool(len(factors) != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: n is not of the form p^k for any prime p and positive integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1