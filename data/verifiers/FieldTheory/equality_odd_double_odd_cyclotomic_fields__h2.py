import sympy
from sympy.ntheory import totient

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be an integer `n` (or a tuple where `n` is the first element).
    """
    try:
        if isinstance(witness, (tuple, list)):
            n_val = witness[0]
        else:
            n_val = witness
        
        n_sym = sympy.sympify(n_val)
        if not n_sym.is_integer:
            return [False, False, False]
        n = int(n_sym)
    except Exception:
        return [False, False, False]

    # H_1: n is an odd positive integer
    try:
        h1_ok = (n > 0) and (n % 2 == 1)
    except Exception:
        h1_ok = False

    # H_2: \zeta_{2n} is a primitive 2n-th root of unity in \mathbb{C}
    # This is a definitional hypothesis that is valid for any positive integer n.
    try:
        h2_ok = (n > 0)
    except Exception:
        h2_ok = False

    # ¬Q: The cyclotomic fields \mathbb{Q}(\zeta_n) and \mathbb{Q}(\zeta_{2n}) are NOT equal.
    # Since \mathbb{Q}(\zeta_n) is always a subfield of \mathbb{Q}(\zeta_{2n}),
    # they are equal if and only if their degrees over \mathbb{Q} are equal.
    # The degree of \mathbb{Q}(\zeta_k) over \mathbb{Q} is totient(k).
    try:
        neg_q_ok = totient(n) != totient(2 * n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: zeta_2n is a primitive 2n-th root of unity in C",
    "¬Q: The cyclotomic fields Q(zeta_n) and Q(zeta_2n) are not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2