import sympy
from sympy import S, Set

R = S.Reals
Z = S.Integers
N = S.Naturals
Q = S.Rationals

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            space = witness[0]
        else:
            space = witness
            
        h1_ok = isinstance(space, Set) and (space.is_subset(S.Reals) == True)
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            space = witness[0]
        else:
            space = witness
            
        if not (isinstance(space, Set) and (space.is_subset(S.Reals) == True)):
            neg_q_ok = False
        else:
            bounded = space.is_bounded
            if bounded is False:
                neg_q_ok = True
            elif bounded is True:
                neg_q_ok = False
            else:
                try:
                    neg_q_ok = (space.inf == S.NegativeInfinity) or (space.sup == S.Infinity)
                except Exception:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X is not totally bounded"
]

N_HYP = 1
NEG_Q_INDEX = 1