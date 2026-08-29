import sympy
from sympy import eye, zeros
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Let R be a right Artinian ring",
    "¬Q: The set S is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    R, S = None, None
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness)
            S = witness.get('S', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            if hasattr(witness, 'R'):
                R = witness.R
            else:
                R = witness
            if hasattr(witness, 'S'):
                S = witness.S
    except Exception:
        pass

    # H_1: R is a right Artinian ring
    h1_ok = False
    try:
        if hasattr(R, 'is_artinian') and R.is_artinian:
            h1_ok = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1_ok = True
        elif hasattr(R, 'is_finite') and R.is_finite:
            h1_ok = True
        elif isinstance(R, str):
            R_str = R.lower()
            if "matrix" in R_str or "m_" in R_str or "field" in R_str or "artinian" in R_str:
                h1_ok = True
            elif "qq" in R_str or "rr" in R_str or "cc" in R_str:
                h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The set S is not finite
    neg_q_ok = False
    try:
        if S is not None:
            if hasattr(S, 'is_finite') and S.is_finite is False:
                neg_q_ok = True
            elif hasattr(S, 'is_infinite') and S.is_infinite is True:
                neg_q_ok = True
            elif isinstance(S, str):
                S_str = S.lower()
                if "infinite" in S_str or "inf" in S_str or "not finite" in S_str:
                    neg_q_ok = True
            elif isinstance(S, type(itertools.count())):
                neg_q_ok = True
        else:
            # If S is not explicitly provided, check if R implies an infinite set of idempotents
            if isinstance(R, str):
                R_str = R.lower()
                if ("matrix" in R_str or "m_" in R_str) and ("qq" in R_str or "rr" in R_str or "cc" in R_str or "field" in R_str or "inf" in R_str):
                    neg_q_ok = True
            elif hasattr(R, 'has_infinite_idempotents') and R.has_infinite_idempotents:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]