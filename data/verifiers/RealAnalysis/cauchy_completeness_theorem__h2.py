import sympy
import math

# Top-level setup: define the index variable for sequences
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every sequence of real numbers converges to a limit in the real numbers."
    (The Cauchy hypothesis was dropped).
    """
    # H_1: (a_n) is a sequence of real numbers
    h1_ok = False
    try:
        if hasattr(witness, 'subs'):
            h1_ok = True
            # Check the first few terms to ensure they evaluate to real numbers
            for i in range(1, 20):
                val = complex(witness.subs(n, i).evalf())
                if abs(val.imag) > 1e-9 or math.isnan(val.real) or math.isinf(val.real):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # ¬Q: The sequence (a_n) does NOT converge to a limit in the real numbers
    neg_q_ok = False
    try:
        L = sympy.limit(witness, n, sympy.oo)
        # A sequence converges to a real limit if the limit is a finite real number.
        # If it's AccumBounds, oo, -oo, or nan, it does not converge to a real number.
        if hasattr(L, 'is_number') and L.is_number and L.is_real and L.is_finite:
            neg_q_ok = False
        else:
            neg_q_ok = True
    except Exception:
        # Fallback: check numerically for divergence or oscillation
        try:
            vals = [float(witness.subs(n, i).evalf()) for i in range(1000, 1050)]
            if max(vals) - min(vals) > 1e-4:
                neg_q_ok = True
            else:
                neg_q_ok = False
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "¬Q: (a_n) does not converge to a limit in the real numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1