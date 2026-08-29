import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        if n < 0:
            neg_q = False
        else:
            # O(n) has 1 connected component if n == 0, and 2 components if n > 0
            components = 1 if n == 0 else 2
            neg_q = (components != 2)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: O(n) does not have exactly two connected components"
]

N_HYP = 0
NEG_Q_INDEX = 0