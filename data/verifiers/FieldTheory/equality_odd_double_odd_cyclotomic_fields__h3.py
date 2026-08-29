import sympy
from sympy.ntheory import totient

# Top-level setup
# (No specific named bindings required for this number theory/field theory conjecture)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            n = witness[0]
        else:
            n = witness
    except Exception:
        n = witness

    # H_1: n is an odd positive integer
    try:
        n_int = int(n)
        h1 = (n_int == n) and (n_int > 0) and (n_int % 2 == 1)
    except Exception:
        h1 = False

    # H_2: zeta_n is a primitive n-th root of unity in C
    # This is a mathematical fact that holds for any positive integer n.
    try:
        n_int = int(n)
        h2 = (n_int == n) and (n_int > 0)
    except Exception:
        h2 = False

    # ¬Q: The cyclotomic fields Q(zeta_n) and Q(zeta_{2n}) are not equal
    try:
        n_int = int(n)
        # Q(zeta_n) is always a subfield of Q(zeta_{2n}).
        # Therefore, they are equal if and only if their degrees over Q are equal.
        # The degree of the k-th cyclotomic field over Q is totient(k).
        deg_n = totient(n_int)
        deg_2n = totient(2 * n_int)
        fields_equal = (deg_n == deg_2n)
        neg_q = not fields_equal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: zeta_n is a primitive n-th root of unity in C",
    "¬Q: The cyclotomic fields Q(zeta_n) and Q(zeta_{2n}) are not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2