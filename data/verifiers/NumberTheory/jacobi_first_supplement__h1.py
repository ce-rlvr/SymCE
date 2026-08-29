import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            h1_ok = False
        else:
            h1_ok = bool(n > 0)
    except Exception:
        h1_ok = False

    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            neg_q_ok = False
        else:
            try:
                lhs = jacobi_symbol(-1, int(n))
                rhs = sympy.S(-1)**((n - sympy.S(1)) / sympy.S(2))
                neg_q_ok = bool(lhs != rhs)
            except ValueError:
                # jacobi_symbol is undefined for even n, so the equality fails
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n > 0",
    "¬Q: (-1/n) != (-1)**((n-1)/2)"
]

N_HYP = 1
NEG_Q_INDEX = 1