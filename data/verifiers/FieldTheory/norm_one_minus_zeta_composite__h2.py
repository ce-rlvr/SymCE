import sympy
from sympy import Symbol, isprime, cyclotomic_poly

# Top-level setup for the namespace
# No specific named bindings are needed for this number theory conjecture.

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the conjecture.
    """
    try:
        # Extract the integer n from the witness
        if isinstance(witness, dict):
            n = int(witness.get('n', witness.get('N', 0)))
        elif isinstance(witness, (tuple, list)):
            n = int(witness[0])
        else:
            n = int(witness)
    except Exception:
        return [False, False, False]

    # H_1: n is a composite integer
    try:
        h1_ok = (n > 1) and not isprime(n)
    except Exception:
        h1_ok = False

    # H_2: zeta_n is a primitive n-th root of unity
    # This is a definitional hypothesis that holds for any valid index n >= 1.
    try:
        h2_ok = (n >= 1)
    except Exception:
        h2_ok = False

    # ¬Q: The field norm N_{Q(zeta_n)/Q}(1 - zeta_n) is NOT equal to 1.
    # The norm of (1 - zeta_n) in Q(zeta_n)/Q is exactly the value of the 
    # n-th cyclotomic polynomial evaluated at x = 1.
    try:
        x = Symbol('x')
        poly = cyclotomic_poly(n, x)
        norm_val = poly.subs(x, 1)
        neg_q_ok = (norm_val != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a composite integer",
    "H_2: zeta_n is a primitive n-th root of unity",
    "¬Q: The field norm N(1-zeta_n) is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2