import sympy
import sympy.ntheory

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            Q = False
        else:
            sig = sympy.ntheory.divisor_sigma(n)
            p_sum = sum(sympy.ntheory.primefactors(n))
            Q = bool(sig > p_sum)
    except Exception:
        Q = False

    neg_Q = not Q
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: sigma(n) <= sum of distinct prime factors of n (or undefined)"
]

N_HYP = 0
NEG_Q_INDEX = 0