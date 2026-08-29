import sympy
import math

# Top-level setup
# (No specific algebraic objects needed for this Real Analysis theorem)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "Delta^n is a compact subset of R^{n+1}"
    
    The standard simplex Delta^n is compact for finite integers n >= -1.
    For n = oo, or non-integer n, it is not a compact subset of R^{n+1}.
    """
    try:
        if witness == sympy.oo or witness == math.inf:
            neg_q = True
        else:
            # Check if witness is an integer
            if float(witness) != int(witness):
                neg_q = True
            else:
                n = int(witness)
                if n >= -1:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Delta^n is not a compact subset of R^{n+1}"
]

N_HYP = 0
NEG_Q_INDEX = 0