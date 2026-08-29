import sympy
from sympy import Set

def get_I(witness):
    if isinstance(witness, dict) and 'I' in witness:
        return witness['I']
    elif isinstance(witness, tuple) and len(witness) == 2:
        return witness[1]
    return witness

def conditions(witness) -> list[bool]:
    try:
        I = get_I(witness)
        h1_ok = isinstance(I, Set)
    except Exception:
        h1_ok = False

    try:
        I = get_I(witness)
        # The conclusion is that I is at most countable.
        # The negation is that I is uncountable.
        neg_q_ok = (I.is_countable is False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is the set of all isolated points of X",
    "¬Q: The set I is uncountable"
]

N_HYP = 1
NEG_Q_INDEX = 1