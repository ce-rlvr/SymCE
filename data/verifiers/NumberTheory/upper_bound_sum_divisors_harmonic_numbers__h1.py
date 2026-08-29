import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        n = witness
        # The hypothesis defines H_n for an integer n
        H_1_ok = isinstance(n, (int, sympy.Integer))
    except Exception:
        H_1_ok = False

    try:
        n = witness
        if not isinstance(n, (int, sympy.Integer)):
            neg_Q_ok = False
        else:
            # Calculate H_n = sum_{k=1}^n 1/k
            # For n <= 0, the range is empty and the sum evaluates to 0
            H_n = sum(sympy.Rational(1, k) for k in range(1, int(n) + 1))
            
            # Calculate sigma(n)
            # sympy's divisor_sigma handles negative integers by taking their absolute value
            sigma_n = divisor_sigma(int(n))
            
            # The conclusion is sigma(n) <= n * H_n
            # We want the negation of the conclusion (i.e., it fails at the witness)
            neg_Q_ok = not bool(sigma_n <= n * H_n)
    except Exception:
        neg_Q_ok = False

    return [H_1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: H_n is the n-th harmonic number",
    "¬Q: sigma(n) > n * H_n"
]

N_HYP = 1
NEG_Q_INDEX = 1