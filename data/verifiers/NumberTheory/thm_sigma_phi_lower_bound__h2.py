import sympy
from sympy.ntheory import divisor_sigma, totient

# Top-level setup for Number Theory (no special named objects required)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        n_sym = sympy.sympify(witness)
        if not n_sym.is_integer:
            h1 = False
        else:
            n = int(n_sym)
            h1 = n > 1
    except Exception:
        h1 = False

    try:
        n_sym = sympy.sympify(witness)
        if not n_sym.is_integer:
            neg_q = False
        else:
            n = int(n_sym)
            # The conclusion is \sigma(n) + \phi(n) >= 2n
            # The negated conclusion is \sigma(n) + \phi(n) < 2n
            neg_q = divisor_sigma(n) + totient(n) < 2 * n
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: \\sigma(n) + \\phi(n) < 2n"
]

N_HYP = 1
NEG_Q_INDEX = 1