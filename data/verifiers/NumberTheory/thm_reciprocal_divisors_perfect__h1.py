import sympy
from sympy.ntheory import divisor_sigma, divisors

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

CONDITION_LABELS = [
    "H_1: sigma(n) == 2n",
    "¬Q: sum(1/d for d in divisors(n)) != 2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        h1 = bool(divisor_sigma(n) == 2 * n)
    except Exception:
        h1 = False

    try:
        n = sympy.sympify(witness)
        divs = divisors(n)
        s = sum(sympy.S(1) / d for d in divs)
        neg_q = bool(s != 2)
    except Exception:
        neg_q = True

    return [h1, neg_q]