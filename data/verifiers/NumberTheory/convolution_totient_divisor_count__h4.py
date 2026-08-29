import sympy

def conditions(witness):
    try:
        h1 = (type(witness) is int or isinstance(witness, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    h2 = True
    h3 = True

    try:
        if h1:
            n = int(witness)
            lhs = sum(sympy.totient(d) * sympy.divisor_count(n // d) for d in sympy.divisors(n))
            rhs = sympy.divisor_sigma(n)
            neg_q = bool(lhs != rhs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: phi(n) is Euler's totient function",
    "H_3: tau(n) is the number of divisors function",
    "¬Q: sum_{d|n} phi(d) tau(n/d) != sigma(n)"
]

N_HYP = 3
NEG_Q_INDEX = 3