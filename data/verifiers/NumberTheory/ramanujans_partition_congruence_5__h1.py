import sympy
from sympy.ntheory import npartitions

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        k = 5 * n + 4
        h1_ok = bool(k.is_integer)
    except Exception:
        h1_ok = False

    try:
        n = sympy.sympify(witness)
        k = 5 * n + 4
        if not k.is_integer:
            neg_q = False
        else:
            p_k = npartitions(int(k))
            neg_q = bool((p_k % 5) != 0)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: p(k) denotes the partition function (5n+4 is an integer)",
    "¬Q: p(5n+4) is not congruent to 0 mod 5"
]

N_HYP = 1
NEG_Q_INDEX = 1