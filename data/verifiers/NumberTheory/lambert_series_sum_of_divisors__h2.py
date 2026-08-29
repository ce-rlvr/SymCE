import sympy
import math

# Top-level setup
# No specific named bindings are needed for this number theory/analysis conjecture.

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: x is a complex number
    try:
        # Check if it's a valid numeric type
        if not isinstance(witness, (int, float, complex, sympy.Expr)):
            h1 = False
        else:
            x = complex(witness)
            h1 = math.isfinite(x.real) and math.isfinite(x.imag)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness
    # The conclusion is the Lambert series identity:
    # \sum_{n=1}^\infty \frac{n x^n}{1-x^n} = \sum_{n=1}^\infty \sigma(n) x^n
    # This identity holds mathematically if and only if |x| < 1.
    # If |x| >= 1, the series diverge and the equality of sums is undefined/false.
    try:
        x = complex(witness)
        if not (math.isfinite(x.real) and math.isfinite(x.imag)):
            neg_q = True
        elif abs(x) >= 1:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        # If we can't evaluate it as a complex number, the equation evaluation fails
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a complex number",
    "¬Q: The Lambert series identity fails (e.g., due to divergence)"
]

N_HYP = 1
NEG_Q_INDEX = 1