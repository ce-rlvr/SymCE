import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = (
            isinstance(witness, PermutationGroup) or 
            type(witness).__name__ in ('FpGroup', 'PolycyclicGroup') or 
            hasattr(witness, 'generators') or 
            hasattr(witness, 'is_group')
        )
    except Exception:
        h1 = False

    # H_2: G is nilpotent
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            h2 = bool(val() if callable(val) else val)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not a polycyclic group
    try:
        is_poly = False
        if hasattr(witness, 'is_polycyclic'):
            val = witness.is_polycyclic
            is_poly = bool(val() if callable(val) else val)
        elif type(witness).__name__ == 'PolycyclicGroup':
            is_poly = True
        elif hasattr(witness, 'is_solvable'):
            # For finite groups (like PermutationGroup), solvable implies polycyclic
            val = witness.is_solvable
            is_poly = bool(val() if callable(val) else val)
        elif type(witness).__name__ == 'FpGroup':
            # FpGroups are finitely generated. Finitely generated nilpotent groups are polycyclic.
            if h2:
                is_poly = True
            else:
                is_poly = False
        else:
            is_poly = False
        
        neg_q = not is_poly
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is nilpotent",
    "¬Q: G is not a polycyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2