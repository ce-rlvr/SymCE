import sympy
from sympy.ntheory import jacobi_symbol

def is_integer(x):
    if isinstance(x, int):
        return True
    if isinstance(x, sympy.Integer):
        return True
    if hasattr(x, 'is_integer') and x.is_integer:
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            n = witness['n']
        else:
            a, b, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_integer(a)
    except Exception:
        h1 = False

    try:
        h2 = is_integer(b)
    except Exception:
        h2 = False

    try:
        lhs = jacobi_symbol(int(a) * int(b), int(n))
        rhs = jacobi_symbol(int(a), int(n)) * jacobi_symbol(int(b), int(n))
        neg_q = (lhs != rhs)
    except Exception:
        # If n is not a positive odd integer, jacobi_symbol raises ValueError in SymPy,
        # meaning the expression is undefined and the equality fails.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: b is an integer",
    "¬Q: The Jacobi symbol (ab/n) is not equal to (a/n) * (b/n) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2