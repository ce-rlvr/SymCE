import sympy

# Top-level setup
# (No specific named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
        else:
            a, b = witness
    except Exception:
        return [False, False]

    try:
        b_sym = sympy.sympify(b)
        h1 = (b_sym.is_integer is True)
    except Exception:
        h1 = False

    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        diff = a_sym - b_sym
        # a == b mod 1 iff (a - b) is an integer
        neg_q = (diff.is_integer is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: b is an integer",
    "¬Q: a is not congruent to b modulo 1"
]

N_HYP = 1
NEG_Q_INDEX = 1