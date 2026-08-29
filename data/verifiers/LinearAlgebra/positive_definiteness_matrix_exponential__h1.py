import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        expA = witness.exp()
        is_sym = (expA == expA.T)
        if not is_sym:
            neg_q = True
        else:
            is_pd = True
            n = expA.shape[0]
            for i in range(1, n + 1):
                det = expA[:i, :i].det()
                
                if det.is_positive is True:
                    continue
                if det.is_positive is False:
                    is_pd = False
                    break
                
                # Fallback for cases where is_positive is None
                try:
                    val = float(det)
                    if val <= 0:
                        is_pd = False
                        break
                except TypeError:
                    try:
                        if not (det > 0):
                            is_pd = False
                            break
                    except Exception:
                        is_pd = False
                        break
            neg_q = not is_pd
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: e^A is not symmetric or not strictly positive definite"
]

N_HYP = 0
NEG_Q_INDEX = 0