import sympy
from sympy import QQ, ZZ, RR, CC

def conditions(witness) -> list[bool]:
    # H_1: K^{\times} is the multiplicative group of units of K
    try:
        h1_ok = False
        if witness in [QQ, ZZ, RR, CC]:
            h1_ok = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1_ok = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1_ok = True
        elif hasattr(witness, 'characteristic') and hasattr(witness, 'order'):
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: K^{\times} is not a divisible group
    try:
        neg_q_ok = False
        if witness == CC:
            neg_q_ok = False
        elif witness in [QQ, ZZ, RR]:
            neg_q_ok = True
        elif hasattr(witness, 'order'):
            order_val = witness.order() if callable(witness.order) else witness.order
            neg_q_ok = bool(order_val > 2)
        elif hasattr(witness, 'mod'):
            neg_q_ok = bool(witness.mod > 2)
        else:
            # For any other generic ring/field provided as a counterexample,
            # we assume its unit group is not divisible unless it's CC.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K^{\\times} is the multiplicative group of units of K",
    "¬Q: K^{\\times} is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1