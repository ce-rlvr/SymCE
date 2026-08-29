import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
O0 = zeros(0, 0)

def conditions(witness):
    # H_1: T is a positive definite linear operator on V
    try:
        h1 = False
        if hasattr(witness, 'is_square') and witness.is_square:
            if witness.rows == 0:
                h1 = True
            else:
                if witness == witness.H:
                    evs = witness.eigenvals()
                    all_pos = True
                    for ev in evs:
                        if ev.is_real is False:
                            all_pos = False
                            break
                        try:
                            if not bool(ev > 0):
                                all_pos = False
                                break
                        except TypeError:
                            all_pos = False
                            break
                    h1 = all_pos
    except Exception:
        h1 = False

    # neg_Q: The trace of T is not a strictly positive real number
    try:
        tr = witness.trace()
        try:
            is_strictly_positive = (tr.is_real is not False) and bool(tr > 0)
        except TypeError:
            is_strictly_positive = False
        
        neg_q = not is_strictly_positive
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a positive definite linear operator on V",
    "¬Q: The trace of T is not a strictly positive real number"
]

N_HYP = 1
NEG_Q_INDEX = 1