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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        is_abelian = False
        try:
            if hasattr(witness, 'is_abelian'):
                is_abelian = bool(witness.is_abelian)
        except Exception:
            pass
            
        if not is_abelian:
            is_projective = False
        else:
            is_projective = False
            try:
                is_finite = False
                if hasattr(witness, 'order') and callable(witness.order):
                    try:
                        order = witness.order()
                        if order != sympy.oo:
                            is_finite = True
                            is_projective = (order == 1)
                    except Exception:
                        pass
                
                if not is_finite and hasattr(witness, 'abelian_invariants') and callable(witness.abelian_invariants):
                    invs = witness.abelian_invariants()
                    is_projective = all(inv == 0 for inv in invs)
            except Exception:
                pass
                
        neg_q = not is_projective
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: F is not a projective object in the category of abelian groups"
]

N_HYP = 0
NEG_Q_INDEX = 0