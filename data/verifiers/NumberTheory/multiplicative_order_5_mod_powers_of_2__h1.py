import sympy
from sympy.ntheory import n_order

CONDITION_LABELS = [
    "H_1: n = 2^k",
    "¬Q: The multiplicative order of 5 modulo n is not exactly 2^{k-2}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        val = sympy.sympify(witness)
        if not val.is_Integer:
            h1 = False
        else:
            n = int(val)
            h1 = (n > 0) and ((n & (n - 1)) == 0)
    except Exception:
        h1 = False

    try:
        val = sympy.sympify(witness)
        if not val.is_Integer:
            neg_q = False
        else:
            n = int(val)
            if (n > 0) and ((n & (n - 1)) == 0):
                k = n.bit_length() - 1
                if n == 1:
                    order = 1
                else:
                    order = n_order(5, n)
                expected = 2**(k - 2)
                neg_q = bool(order != expected)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]