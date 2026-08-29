import sympy

x = sympy.Symbol('x')
t = sympy.Symbol('t')

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(witness.domain.is_Field)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (witness.degree() == 2) and bool(witness.is_irreducible)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(witness.diff().is_zero)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a field extension of F such that the degree is exactly 2",
    "¬Q: E is not a Galois extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2