import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            m = witness['m']
            n = witness['n']
        else:
            a, m, n = witness
    except Exception:
        return [False, False, False]

    # H1: a is an integer
    try:
        h1 = isinstance(a, int) or (hasattr(a, 'is_integer') and a.is_integer)
    except Exception:
        h1 = False

    # H2: n is an odd positive integer
    try:
        h2 = (isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)) and int(n) % 2 == 1 and int(n) > 0
    except Exception:
        h2 = False

    # neg_Q: The Jacobi symbol (a/mn) is equal to the product (a/m)(a/n)
    try:
        if not (isinstance(m, int) or (hasattr(m, 'is_integer') and m.is_integer)):
            neg_q = True
        else:
            left = jacobi_symbol(int(a), int(m * n))
            right = jacobi_symbol(int(a), int(m)) * jacobi_symbol(int(a), int(n))
            neg_q = (left != right)
    except Exception:
        # If jacobi_symbol raises ValueError (e.g., m is even or negative), the expression is undefined.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: n is an odd positive integer",
    "¬Q: The Jacobi symbol (a/mn) is not equal to the product (a/m)(a/n) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2