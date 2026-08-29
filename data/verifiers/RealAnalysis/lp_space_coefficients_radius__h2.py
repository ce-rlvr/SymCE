import sympy
from sympy import Symbol, oo, limit, Abs

n = Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    try:
        val = witness.subs(n, 2)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        a_n = witness
        a_n_plus_1 = witness.subs(n, n + 1)
        R = limit(Abs(a_n / a_n_plus_1), n, oo)
        neg_q_ok = bool(R < 1)
    except Exception:
        try:
            L = limit(Abs(witness)**(1/n), n, oo)
            if L == oo:
                R = 0
            elif L == 0:
                R = oo
            else:
                R = 1 / L
            neg_q_ok = bool(R < 1)
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series",
    "¬Q: The radius of convergence is strictly less than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1