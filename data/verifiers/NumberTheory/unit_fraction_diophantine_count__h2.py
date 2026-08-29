import sympy
from sympy.ntheory import divisor_count

# No specific named objects are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    # Extract n and S from the witness
    try:
        if isinstance(witness, dict):
            n = witness['n']
            S = witness['S']
        elif hasattr(witness, 'n') and hasattr(witness, 'S'):
            n = witness.n
            S = witness.S
        else:
            n, S = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # ¬Q: The cardinality of S is NOT equal to the number of positive divisors of n^2
    try:
        if hasattr(S, 'cardinality'):
            card_S = S.cardinality()
        elif hasattr(S, '__len__'):
            card_S = len(S)
        else:
            card_S = None
            
        if card_S is not None:
            expected = divisor_count(n**2)
            neg_q = (card_S != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The cardinality of S is not equal to the number of positive divisors of n^2"
]

N_HYP = 1
NEG_Q_INDEX = 1