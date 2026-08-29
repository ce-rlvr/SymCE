import sympy
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H1: A is invertible
    try:
        if not hasattr(witness, 'inv'):
            h1_ok = False
        else:
            # Attempt to invert the matrix; succeeds if invertible
            witness.inv()
            h1_ok = True
    except Exception:
        h1_ok = False

    # Q: sigma_min(A) <= |det(A)|^(1/n)
    try:
        n = witness.shape[0]
        sv = witness.singular_values()
        min_sv = min(sv)
        det_val = sympy.Abs(witness.det())
        
        # This will intentionally raise ZeroDivisionError if n=0,
        # correctly marking the conclusion as failed (undefined).
        rhs = det_val ** sympy.Rational(1, n)
        
        rel = min_sv <= rhs
        if rel == True:
            q_ok = True
        elif rel == False:
            q_ok = False
        else:
            q_ok = bool(rel.evalf())
    except Exception:
        # If the conclusion is undefined (e.g., n=0, empty singular values), it fails.
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is invertible",
    "¬Q: sigma_min(A) <= |det(A)|^(1/n) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1