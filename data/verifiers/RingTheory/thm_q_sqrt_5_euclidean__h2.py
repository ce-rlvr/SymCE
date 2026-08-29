import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import re

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    h1 = False
    try:
        # Check if the witness represents the real quadratic field Q(sqrt(5))
        s = str(witness).replace(' ', '')
        if s in ('5', 'sqrt(5)', 'Q(sqrt(5))', 'QQ(sqrt(5))', 'Z[sqrt(5)]', 'Z[(1+sqrt(5))/2]'):
            h1 = True
        elif witness == sympy.sqrt(5):
            h1 = True
        elif witness == 5:
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if h1:
            # For K = Q(sqrt(5)), O_K is Z[(1+sqrt(5))/2], which IS a Euclidean domain.
            # Therefore, the conclusion holds, and its negation is False.
            neg_q = False
        else:
            # Fallback evaluation for other quadratic fields Q(sqrt(d))
            s = str(witness).replace('**2', '').replace('^2', '')
            nums = re.findall(r'-?\d+', s)
            if nums:
                d = int(nums[-1])
                # If given as a minimal polynomial like x**2 - d
                if 'x' in s and d < 0:
                    d = -d
                
                # Known squarefree d for which O_K is a Euclidean domain
                euclidean_d = {
                    -11, -7, -3, -2, -1, 
                    2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73
                }
                if d not in euclidean_d:
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the real quadratic field Q(sqrt(5))",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1