import sympy
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.shape[0] == witness.shape[1]
    except Exception:
        h1 = False

    try:
        if not h1 or witness.shape[0] == 0:
            neg_q = False
        else:
            evs = witness.eigenvals()
            rho_val = max([float(sympy.Abs(ev).evalf()) for ev in evs.keys()])
            
            A_star_A = witness.H * witness
            sv2 = A_star_A.eigenvals()
            sigma_max_val = math.sqrt(max([float(sympy.Abs(ev).evalf()) for ev in sv2.keys()]))
            
            # The conclusion is sigma_max(A) >= rho(A).
            # The negation is sigma_max(A) < rho(A).
            # We use a small tolerance to avoid false positives due to floating point inaccuracies.
            neg_q = bool(sigma_max_val < rho_val * (1 - 1e-9) - 1e-12)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The maximum singular value sigma_max(A) is strictly less than rho(A)"
]

N_HYP = 1
NEG_Q_INDEX = 1