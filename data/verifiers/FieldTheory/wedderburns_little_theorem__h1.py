import sympy
from sympy import QQ, ZZ, RR, CC
from sympy import Quaternion

class QuaternionAlgebra:
    def __init__(self):
        self.is_division_ring = True
        self.is_commutative = False
        self.is_Field = False

# Top-level setup for potential witness expressions
H = QuaternionAlgebra()
Quaternions = H

def conditions(witness) -> list[bool]:
    # H_1: R is a division ring
    try:
        if witness is Quaternion or isinstance(witness, Quaternion):
            h1 = True
        elif isinstance(witness, str) and witness.lower() in ['h', 'quaternions', 'quaternion']:
            h1 = True
        elif hasattr(witness, 'is_division_ring'):
            h1 = bool(witness.is_division_ring)
        elif hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: R is not a commutative field
    try:
        if witness is Quaternion or isinstance(witness, Quaternion):
            neg_q = True
        elif isinstance(witness, str) and witness.lower() in ['h', 'quaternions', 'quaternion']:
            neg_q = True
        else:
            if hasattr(witness, 'is_commutative'):
                is_comm = bool(witness.is_commutative)
            elif hasattr(witness, 'is_Field'):
                is_comm = True
            else:
                is_comm = True
            
            if hasattr(witness, 'is_Field'):
                is_field = bool(witness.is_Field)
            elif hasattr(witness, 'is_division_ring'):
                is_field = bool(witness.is_division_ring) and is_comm
            else:
                is_field = False
                
            neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a division ring",
    "¬Q: R is not a commutative field"
]

N_HYP = 1
NEG_Q_INDEX = 1