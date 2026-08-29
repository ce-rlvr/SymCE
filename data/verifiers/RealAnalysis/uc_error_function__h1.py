import sympy
import math

CONDITION_LABELS = [
    "¬Q: erf(x) is not uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    """
    Checks if the witness demonstrates that erf(x) is NOT uniformly continuous on R.
    Since erf(x) IS uniformly continuous on R, a valid witness should not exist,
    but we evaluate the mathematical conditions for a counterexample anyway.
    
    A counterexample can be provided as:
      1. A tuple (x_n, y_n, epsilon) where x_n and y_n are sympy expressions in 'n',
         lim_{n->oo} (x_n - y_n) = 0, and lim_{n->oo} |erf(x_n) - erf(y_n)| >= epsilon > 0.
      2. A tuple (epsilon, f_delta) where f_delta is a function that takes delta > 0
         and returns (x, y) such that |x - y| < delta and |erf(x) - erf(y)| >= epsilon > 0.
    """
    neg_q = False
    
    # Approach 1: Witness is (x_n, y_n, epsilon) as sympy expressions of 'n'
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            x_n, y_n, eps = witness
            n = sympy.Symbol('n')
            if eps > 0:
                diff_lim = sympy.limit(x_n - y_n, n, sympy.oo)
                if diff_lim == 0:
                    erf_diff_lim = sympy.limit(sympy.Abs(sympy.erf(x_n) - sympy.erf(y_n)), n, sympy.oo)
                    if erf_diff_lim >= eps:
                        neg_q = True
    except Exception:
        pass

    # Approach 2: Witness is (epsilon, f_delta) where f_delta(delta) -> (x, y)
    if not neg_q:
        try:
            if isinstance(witness, tuple) and len(witness) == 2:
                eps, f_delta = witness
                if eps > 0:
                    deltas = [1.0, 0.1, 0.01, 0.001, 0.0001]
                    all_valid = True
                    for d in deltas:
                        x, y = f_delta(d)
                        if abs(x - y) >= d:
                            all_valid = False
                            break
                        val_x = float(sympy.erf(x).evalf())
                        val_y = float(sympy.erf(y).evalf())
                        if abs(val_x - val_y) < eps:
                            all_valid = False
                            break
                    if all_valid:
                        neg_q = True
        except Exception:
            pass

    return [bool(neg_q)]