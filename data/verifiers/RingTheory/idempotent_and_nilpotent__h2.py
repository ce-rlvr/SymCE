import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: e is an element of a ring
    try:
        zero = witness * 0
        _ = witness + witness
        _ = witness * witness
        h1 = True
    except Exception:
        h1 = False

    # H_2: e is nilpotent (e^n = 0 for some n >= 1)
    try:
        h2 = False
        zero = witness * 0
        curr = witness
        for _ in range(1, 100):
            if curr == zero:
                h2 = True
                break
            curr = curr * witness
    except Exception:
        h2 = False

    # ¬Q: e is not 0
    try:
        zero = witness * 0
        neg_q = bool(witness != zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: e is an element of a ring",
    "H_2: e is nilpotent",
    "¬Q: e is not 0"
]

N_HYP = 2
NEG_Q_INDEX = 2