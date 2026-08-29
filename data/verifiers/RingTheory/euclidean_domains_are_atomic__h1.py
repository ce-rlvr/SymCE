import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_atomic'):
            is_atom = witness.is_atomic() if callable(witness.is_atomic) else witness.is_atomic
            neg_q = not bool(is_atom)
        elif hasattr(witness, 'is_UFD') and witness.is_UFD:
            neg_q = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif hasattr(witness, 'is_PID') and witness.is_PID:
            neg_q = False
        elif isinstance(witness, str):
            neg_q = "non-atomic" in witness.lower() or "not atomic" in witness.lower()
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: R is not an atomic domain"]
N_HYP = 0
NEG_Q_INDEX = 0