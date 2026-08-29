import sympy
from sympy import Rational

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        n_sym = sympy.sympify(witness)
        if not n_sym.is_integer:
            return [False, False]
        n = int(n_sym)
    except Exception:
        return [False, False]

    # H_1: n > 1
    try:
        h1 = bool(n > 1)
    except Exception:
        h1 = False

    # neg_Q: sigma(n) >= n * prod_{p|n} p/(p-1)
    try:
        if n < 1:
            neg_q = False
        else:
            sigma_n = sympy.divisor_sigma(n)
            factors = sympy.primefactors(n)
            prod = Rational(1, 1)
            for p in factors:
                prod *= Rational(p, p - 1)
            rhs = n * prod
            neg_q = bool(sigma_n >= rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1",
    "¬Q: sigma(n) >= n * prod_{p|n} p/(p-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1