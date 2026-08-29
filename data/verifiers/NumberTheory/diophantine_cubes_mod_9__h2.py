import sympy

def is_integer(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, sympy.Integer)):
        return True
    try:
        return int(v) == v
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            n = witness['n']
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            witness_list = list(witness)
            if len(witness_list) == 3:
                x, y, n = witness_list
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = is_integer(x) and is_integer(y) and is_integer(n)
    except Exception:
        h1 = False

    try:
        if h1:
            neg_q = (int(x)**3 + int(y)**3 == int(n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y, and n are integers",
    "¬Q: x^3 + y^3 == n"
]

N_HYP = 1
NEG_Q_INDEX = 1