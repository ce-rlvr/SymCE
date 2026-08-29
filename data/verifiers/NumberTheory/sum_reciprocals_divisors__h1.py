import sympy
from sympy import divisors, divisor_sigma, Rational

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is an integer type
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = sympy.Integer(witness)
            h1 = (n != 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = sympy.Integer(witness)
            # LHS: sum of 1/d for all positive divisors d of n
            lhs = sum(Rational(1, d) for d in divisors(n))
            # RHS: sigma(n) / n
            rhs = Rational(divisor_sigma(n), n)
            
            # The conclusion fails if LHS != RHS
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-zero integer",
    "¬Q: sum_{d|n} 1/d != sigma(n)/n"
]

N_HYP = 1
NEG_Q_INDEX = 1