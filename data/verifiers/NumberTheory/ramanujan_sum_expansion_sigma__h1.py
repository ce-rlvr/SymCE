import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims that for all n, sigma(n) = (pi^2 / 6) * n * Sum(c_m(n) / m^2).
    This fails for n <= 0.
    """
    try:
        n = int(witness)
    except Exception:
        return [False]

    try:
        if n == 0:
            # For n = 0, c_m(0) = phi(m), and the sum Sum(phi(m)/m^2) diverges.
            # Thus the right-hand side is undefined, and the equality fails.
            neg_q = True
        else:
            # For n != 0, c_m(n) = c_m(|n|).
            # The infinite sum Sum(c_m(n)/m^2) evaluates exactly to (6/pi^2) * sigma(|n|) / |n|.
            # Therefore, the RHS evaluates to (pi^2/6) * n * (6/pi^2) * sigma(|n|) / |n| = n * sigma(|n|) / |n|.
            lhs = divisor_sigma(n)
            rhs = n * divisor_sigma(abs(n)) // abs(n)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(n) != (pi^2/6) * n * Sum_{m=1}^infty c_m(n)/m^2"
]

N_HYP = 0
NEG_Q_INDEX = 0