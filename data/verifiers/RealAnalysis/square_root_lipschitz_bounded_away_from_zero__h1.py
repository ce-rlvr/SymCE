import sympy
from sympy import oo

def conditions(witness) -> list[bool]:
    try:
        a = sympy.sympify(witness)
        if a.is_number and a.is_real:
            h1_ok = bool(a >= 0)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        a = sympy.sympify(witness)
        if a.is_number and a.is_real:
            # The function f(x) = sqrt(x) is globally Lipschitz on [a, oo) iff a > 0.
            # Therefore, it is NOT globally Lipschitz (conclusion fails) iff a <= 0.
            # Since we only care about cases where it is defined (a >= 0), a == 0 is the counterexample.
            neg_q_ok = bool(a == 0)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) = sqrt(x) is defined on [a, oo) (i.e., a >= 0)",
    "¬Q: f is not globally Lipschitz continuous on [a, oo)"
]

N_HYP = 1
NEG_Q_INDEX = 1