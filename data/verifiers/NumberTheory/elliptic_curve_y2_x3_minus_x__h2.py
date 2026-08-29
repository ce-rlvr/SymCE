import sympy
from sympy import Integer

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two integers (x, y).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1 = False
        else:
            x, y = witness
            h1 = isinstance(x, (int, Integer)) and isinstance(y, (int, Integer))
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            neg_q = False
        else:
            x, y = witness
            # The conclusion is that (x, y) is in {(0,0), (1,0), (-1,0)}.
            # The negated conclusion is that (x, y) is NOT in this set.
            neg_q = (x, y) not in [(0, 0), (1, 0), (-1, 0)]
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y are integers",
    "¬Q: (x, y) is not in {(0,0), (1,0), (-1,0)}"
]

N_HYP = 1
NEG_Q_INDEX = 1