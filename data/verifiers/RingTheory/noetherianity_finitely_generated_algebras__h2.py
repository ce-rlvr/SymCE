import sympy
from sympy import symbols

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            return [
                bool(witness.get('is_R_commutative_Noetherian', False)),
                bool(witness.get('is_A_fg_R_algebra', False)),
                not bool(witness.get('is_A_Noetherian', True))
            ]
        return [
            bool(getattr(witness, 'is_R_commutative_Noetherian', False)),
            bool(getattr(witness, 'is_A_fg_R_algebra', False)),
            not bool(getattr(witness, 'is_A_Noetherian', True))
        ]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: A is finitely generated as an algebra over R",
    "¬Q: A is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2