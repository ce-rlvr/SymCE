import sympy
from sympy.ntheory import isprime

# Top-level setup
# (No named bindings needed for this domain)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            p = witness['p']
        else:
            x, y, p = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number such that p = 3 (mod 4)
    try:
        p_val = sympy.sympify(p)
        h1 = bool(p_val.is_integer and isprime(int(p_val)) and int(p_val) % 4 == 3)
    except Exception:
        h1 = False

    # H_2: x^2 + y^2 = p^2
    try:
        x_val = sympy.sympify(x)
        y_val = sympy.sympify(y)
        p_val = sympy.sympify(p)
        h2 = bool(x_val**2 + y_val**2 == p_val**2)
    except Exception:
        h2 = False

    # ¬Q: x != 0 and y != 0
    try:
        x_val = sympy.sympify(x)
        y_val = sympy.sympify(y)
        neg_q = bool(x_val != 0 and y_val != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number such that p = 3 (mod 4)",
    "H_2: x^2 + y^2 = p^2",
    "¬Q: x != 0 and y != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2