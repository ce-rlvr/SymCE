import sympy
from sympy import symbols

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.get('is_commutative', False) and witness.get('is_noetherian', False))
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.get('krull_dimension') is not None and witness.get('krull_dimension') == witness.get('d'))
    except Exception:
        h2 = False

    try:
        neg_q = bool(witness.get('d') is not None and witness.get('min_gens_m_primary') is not None and witness.get('d') != witness.get('min_gens_m_primary'))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: The Krull dimension of R is d",
    "¬Q: d is not equal to the minimum number of generators required to generate an m-primary ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2