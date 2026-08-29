import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup, free_group
)
from sympy.matrices import eye, zeros
from sympy import oo

# Standard finite groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard infinite groups
Z_group = free_group("x")[0]
Z2_free = free_group("x, y")[0]

def conditions(witness):
    # H_1: G is a nilpotent group
    h1_ok = False
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            if callable(val):
                h1_ok = bool(val())
            else:
                h1_ok = bool(val)
        elif type(witness).__name__ == 'FreeGroup':
            # A free group is nilpotent iff its rank is 0 or 1
            h1_ok = len(witness.generators) <= 1
        elif type(witness).__name__ == 'FpGroup':
            # Check if abelian (which is sufficient for nilpotency)
            gens = witness.generators
            is_ab = True
            for x in gens:
                for y in gens:
                    if x * y != y * x:
                        is_ab = False
                        break
                if not is_ab:
                    break
            if is_ab:
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: G is NOT a torsion group
    neg_q_ok = False
    try:
        is_torsion = False
        
        if hasattr(witness, 'is_finite'):
            val = witness.is_finite
            if callable(val):
                if val(): is_torsion = True
            else:
                if val: is_torsion = True
        
        if not is_torsion and isinstance(witness, PermutationGroup):
            is_torsion = True
            
        if not is_torsion and type(witness).__name__ == 'FreeGroup':
            if len(witness.generators) == 0:
                is_torsion = True
            else:
                is_torsion = False
                
        if not is_torsion and type(witness).__name__ == 'FpGroup':
            try:
                if witness.order() < oo:
                    is_torsion = True
            except Exception:
                pass
                
        neg_q_ok = not is_torsion
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not a torsion group"
]

N_HYP = 1
NEG_Q_INDEX = 1