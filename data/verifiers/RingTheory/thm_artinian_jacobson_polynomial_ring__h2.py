import sympy
from sympy import symbols

x = symbols('x')

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_right_artinian'):
            h1 = bool(witness.is_right_artinian())
        elif hasattr(witness, 'is_artinian'):
            h1 = bool(witness.is_artinian())
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'jacobson_radical_polynomial_ring_eq_ideal'):
            neg_q = not bool(witness.jacobson_radical_polynomial_ring_eq_ideal())
        elif hasattr(witness, 'J_Rx_equals_JR_x'):
            neg_q = not bool(witness.J_Rx_equals_JR_x())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The Jacobson radical of the polynomial ring over R is not exactly the polynomial ring over J(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1