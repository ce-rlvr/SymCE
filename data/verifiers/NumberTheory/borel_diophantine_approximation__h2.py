import sympy
from sympy import S, sympify, simplify

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide an irrational number x and three convergents.
    """
    try:
        # Parse witness
        if hasattr(witness, 'x') and hasattr(witness, 'convergents'):
            x = witness.x
            convergents = witness.convergents
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                x, convergents = witness
            elif len(witness) == 4:
                x = witness[0]
                convergents = witness[1:]
            else:
                return [False, False]
        else:
            return [False, False]
        
        x = sympify(x)
        convergents = [sympify(c) for c in convergents]
        if len(convergents) != 3:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: x is an irrational number
    try:
        h1 = x.is_irrational
        if h1 is None:
            if x.is_real is True and x.is_rational is False:
                h1 = True
            else:
                h1 = False
        h1 = bool(h1)
    except Exception:
        h1 = False

    # neg_Q: None of the three convergents satisfies |x - p_k/q_k| < 1/(sqrt(5)*q_k^2)
    try:
        neg_q = True
        for c in convergents:
            q = c.q
            diff_sq = (x - c)**2
            threshold = S(1) / (5 * q**4)
            
            # We want to check if diff_sq < threshold.
            # If it is strictly less, the conclusion holds for this convergent, so neg_Q is False.
            diff_val = (diff_sq - threshold).evalf(100)
            
            if diff_val < -1e-90:
                neg_q = False
                break
            elif diff_val > 1e-90:
                continue
            else:
                # Fallback to exact symbolic comparison if extremely close to 0
                exact_diff = simplify(diff_sq - threshold)
                if exact_diff.is_negative:
                    neg_q = False
                    break
                elif exact_diff.is_negative is None:
                    if exact_diff.evalf(200) < 0:
                        neg_q = False
                        break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "¬Q: None of the three convergents satisfies |x - p_k/q_k| < 1/(sqrt(5)*q_k^2)"
]

N_HYP = 1
NEG_Q_INDEX = 1