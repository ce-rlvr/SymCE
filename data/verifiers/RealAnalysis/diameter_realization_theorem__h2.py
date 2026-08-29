import sympy
from sympy import Set, S, Interval, FiniteSet, Union, Intersection

Reals = S.Reals
EmptySet = S.EmptySet

def conditions(witness):
    try:
        h1 = isinstance(witness, Set) and (witness.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        elif witness.is_empty == True:
            neg_q = True
        else:
            inf_K = witness.inf
            sup_K = witness.sup
            if inf_K == S.NegativeInfinity or sup_K == S.Infinity:
                neg_q = True
            else:
                has_inf = (witness.contains(inf_K) == True)
                has_sup = (witness.contains(sup_K) == True)
                neg_q = not (has_inf and has_sup)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a metric space (witness is a subset of Reals)",
    "¬Q: The diameter of K is infinite, or there are no x, y in K achieving the diameter"
]

N_HYP = 1
NEG_Q_INDEX = 1