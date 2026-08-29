import sympy
import math
from sympy.ntheory import continued_fraction_periodic

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and fails the conclusion.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H1: d is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = int(witness) > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: d is not a perfect square
    try:
        w = sympy.sympify(witness)
        root = sympy.sqrt(w)
        # If root.is_rational is True, it's a perfect square (or square of a rational)
        h2 = not root.is_rational
    except Exception:
        h2 = False

    # neg_Q: The partial quotients DO NOT satisfy a_i = a_{k-i} for 1 <= i <= k-1, and a_k = 2a_0
    try:
        w = sympy.sympify(witness)
        if w <= 0:
            neg_q = False
        else:
            num, den = w.as_numer_denom()
            # Compute the continued fraction of sqrt(num/den) = sqrt(num*den) / den
            non_per, per = continued_fraction_periodic(0, den, num * den)
            
            conclusion_holds = True
            
            # The standard form for sqrt(d) has exactly one non-periodic term (a_0)
            if len(non_per) != 1:
                conclusion_holds = False
            elif len(per) == 0:
                conclusion_holds = False
            else:
                a_0 = non_per[0]
                k = len(per)
                
                # Check a_k = 2a_0 (in 0-indexed python, a_k is per[-1])
                if per[-1] != 2 * a_0:
                    conclusion_holds = False
                else:
                    # Check a_i = a_{k-i} for 1 <= i <= k-1
                    for i in range(1, k):
                        if per[i-1] != per[k-i-1]:
                            conclusion_holds = False
                            break
                            
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer",
    "H_2: d is not a perfect square",
    "¬Q: The partial quotients do not satisfy a_i = a_{k-i} for 1 <= i <= k-1, and a_k = 2a_0"
]

N_HYP = 2
NEG_Q_INDEX = 2