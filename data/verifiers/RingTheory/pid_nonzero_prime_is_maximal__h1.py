import sympy
from sympy import symbols, ZZ, QQ
from sympy.polys.rings import ring

# Top-level setup: named object bindings
x, y, z = symbols('x y z')
R_Zx, X_Zx = ring('x', ZZ)
R_Qxy, X_Qxy, Y_Qxy = ring('x, y', QQ)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the conjecture:
    'Let P be a non-zero prime ideal of R. Then P is a maximal ideal of R.'
    """
    # H_1: P is a non-zero ideal
    try:
        is_zero_attr = witness.is_zero
        is_zero_val = is_zero_attr() if callable(is_zero_attr) else is_zero_attr
        h1_ok = not bool(is_zero_val)
    except Exception:
        h1_ok = False

    # H_2: P is a prime ideal
    try:
        is_prime_attr = witness.is_prime
        is_prime_val = is_prime_attr() if callable(is_prime_attr) else is_prime_attr
        h2_ok = bool(is_prime_val)
    except Exception:
        h2_ok = False

    # neg_Q: P is NOT a maximal ideal
    try:
        is_maximal_attr = witness.is_maximal
        is_maximal_val = is_maximal_attr() if callable(is_maximal_attr) else is_maximal_attr
        neg_q_ok = not bool(is_maximal_val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a non-zero ideal",
    "H_2: P is a prime ideal",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2