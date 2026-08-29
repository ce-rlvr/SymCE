import sympy
from sympy import S, Set, FiniteSet

# Top-level setup
N = S.Naturals
Z = S.Integers
Q = S.Rationals
R = S.Reals
Empty = S.EmptySet

def conditions(witness) -> list[bool]:
    # H1: X is a metric space
    try:
        if isinstance(witness, (set, list, tuple, frozenset)):
            h1_ok = True
        elif isinstance(witness, Set):
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: X is a countable set
    try:
        if isinstance(witness, (set, list, tuple, frozenset)):
            h2_ok = True
        elif isinstance(witness, Set):
            if witness.is_countable == True:
                h2_ok = True
            elif witness.is_finite == True:
                h2_ok = True
            else:
                h2_ok = False
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The cardinality of X is strictly greater than 1
    try:
        if isinstance(witness, (set, frozenset)):
            neg_q_ok = len(witness) > 1
        elif isinstance(witness, (list, tuple)):
            neg_q_ok = len(set(witness)) > 1
        elif isinstance(witness, Set):
            if witness.is_empty == True:
                neg_q_ok = False
            elif witness.is_finite == True:
                try:
                    neg_q_ok = len(witness) > 1
                except TypeError:
                    neg_q_ok = len(list(witness)) > 1
            elif witness.is_finite == False:
                neg_q_ok = True
            else:
                neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: X is a countable set",
    "¬Q: The cardinality of X is strictly greater than 1"
]

N_HYP = 2
NEG_Q_INDEX = 2