import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Attempt to convert lists, tuples, or other non-SymPy objects to a SymPy Matrix
    try:
        if not hasattr(witness, 'eigenvals'):
            T = sympy.Matrix(witness)
        else:
            T = witness
    except Exception:
        T = witness

    # H_1: V is a finite-dimensional vector space over K
    try:
        h1_ok = hasattr(T, 'shape') and len(T.shape) == 2
    except Exception:
        h1_ok = False

    # H_2: T is a linear operator on V (represented by a square matrix)
    try:
        h2_ok = h1_ok and getattr(T, 'is_square', False)
    except Exception:
        h2_ok = False

    # H_3: The only eigenvalue of T in K is 0
    # We check if the only real eigenvalue is 0, OR the only rational eigenvalue is 0.
    # This accommodates counterexamples over K=R as well as K=Q.
    try:
        if h2_ok:
            evs = T.eigenvals()
            real_evs = {ev for ev in evs if ev.is_real == True}
            rat_evs = {ev for ev in evs if ev.is_rational == True}
            h3_ok = (real_evs == {0}) or (rat_evs == {0})
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: T is not a nilpotent operator
    try:
        if h2_ok:
            n = T.shape[0]
            if n == 0:
                neg_q_ok = False
            else:
                neg_q_ok = not (T**n).is_zero_matrix
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over K",
    "H_2: T is a linear operator on V",
    "H_3: The only eigenvalue of T in K is 0",
    "¬Q: T is not a nilpotent operator"
]

N_HYP = 3
NEG_Q_INDEX = 3