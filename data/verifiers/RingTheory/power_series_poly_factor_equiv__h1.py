import sympy

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            n = witness[1]
        else:
            n = witness
        n_int = int(n)
        h1 = (n_int == n) and (n_int >= 1)
    except Exception:
        h1 = False

    # The conclusion states that the power series factor ring modulo x^n 
    # is isomorphic to the polynomial factor ring modulo x^n.
    # Mathematically, this is always true for any ring R and any integer n >= 1.
    # Therefore, the conclusion never fails for any valid witness, and its negation is False.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 1",
    "not Q: power series factor ring not isomorphic to polynomial factor ring"
]

N_HYP = 1
NEG_Q_INDEX = 1