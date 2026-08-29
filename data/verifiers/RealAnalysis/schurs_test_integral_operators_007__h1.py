import math

# Top-level setup
# No specific named objects are required for this real analysis theorem,
# but we provide standard bindings just in case the witness uses them.
import sympy as sp
from sympy import Rational

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be an object or dictionary containing:
      - K: a 2D list or matrix representing the non-negative kernel K(x, y)
      - f: a 1D list or vector representing the function f(y)
      - p: a number > 1
      - q: a number such that 1/p + 1/q = 1
      - C1: a positive number bounding the column sums (integral over X)
      - C2: a positive number bounding the row sums (integral over Y)
    """
    try:
        if isinstance(witness, dict):
            K = witness['K']
            f = witness['f']
            p = witness['p']
            q = witness['q']
            C1 = witness['C1']
            C2 = witness['C2']
        else:
            K = witness.K
            f = witness.f
            p = witness.p
            q = witness.q
            C1 = witness.C1
            C2 = witness.C2

        # Convert to floats for numerical checking
        p_val = float(p)
        q_val = float(q)
        C1_val = float(C1)
        C2_val = float(C2)

        num_rows = len(K)
        num_cols = len(K[0])

        # H_1: K(x, y) is a non-negative measurable function
        h1 = all(float(K[i][j]) >= 0 for i in range(num_rows) for j in range(num_cols))

        # H_2: integral of K over X is bounded by C1 for almost all y
        # In the discrete case, this is the sum over rows for each column
        h2 = all(sum(float(K[i][j]) for i in range(num_rows)) <= C1_val + 1e-7 for j in range(num_cols))

        # H_3: integral of K over Y is bounded by C2 for almost all x
        # In the discrete case, this is the sum over columns for each row
        h3 = all(sum(float(K[i][j]) for j in range(num_cols)) <= C2_val + 1e-7 for i in range(num_rows))

        # H_4: 1 < p < infinity and 1/p + 1/q = 1
        h4 = p_val > 1 and abs(1.0 / p_val + 1.0 / q_val - 1.0) < 1e-7

        # neg_Q: ||Tf||_p > C1^{1/p} C2^{1/q} ||f||_p
        # Tf(x) = sum_y K(x, y) f(y)
        Tf = [sum(float(K[i][j]) * float(f[j]) for j in range(num_cols)) for i in range(num_rows)]
        
        norm_Tf = sum(abs(x)**p_val for x in Tf)**(1.0 / p_val)
        norm_f = sum(abs(float(y))**p_val for y in f)**(1.0 / p_val)
        
        bound = (C1_val**(1.0 / p_val)) * (C2_val**(1.0 / q_val)) * norm_f
        
        # The conclusion FAILS if the actual norm strictly exceeds the bound
        neg_q = norm_Tf > bound + 1e-7

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: K(x, y) is a non-negative measurable function",
    "H_2: There exists C1 > 0 such that integral of K over X <= C1 for almost all y",
    "H_3: There exists C2 > 0 such that integral of K over Y <= C2 for almost all x",
    "H_4: 1 < p < infinity and 1/p + 1/q = 1",
    "¬Q: ||Tf||_p > C1^{1/p} C2^{1/q} ||f||_p"
]

N_HYP = 4
NEG_Q_INDEX = 4