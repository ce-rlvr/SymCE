import sympy
from sympy.ntheory import jacobi_symbol

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness):
    try:
        # Witness must be an integer
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            return [False, False]
        n = int(witness)
    except Exception:
        return [False, False]

    try:
        h1 = bool(n > 0)
    except Exception:
        h1 = False

    try:
        # The conclusion is (2/n) == (-1)**((n**2-1)/8)
        # The Jacobi symbol (a/n) is only defined for positive odd integers n.
        # If n is even, the Jacobi symbol is undefined, so the equality fails.
        if n % 2 == 0:
            neg_q = True
        else:
            lhs = jacobi_symbol(2, n)
            rhs = (-1)**((n**2 - 1) // 8)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n > 0",
    "¬Q: (2/n) != (-1)^((n^2-1)/8) or undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1