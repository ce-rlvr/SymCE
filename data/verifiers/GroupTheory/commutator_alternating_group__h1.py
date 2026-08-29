import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    h1 = False
    neg_q = False
    
    An = None
    
    try:
        # The witness can be an integer n (representing A_n) or the group A_n itself.
        if isinstance(witness, (int, float)) and not isinstance(witness, bool):
            if float(witness).is_integer():
                n = int(witness)
                if n >= 1:
                    h1 = True
                    An = AlternatingGroup(n)
        elif hasattr(witness, 'degree') and hasattr(witness, 'order') and hasattr(witness, 'derived_subgroup'):
            n = witness.degree
            if n >= 1:
                An_ref = AlternatingGroup(n)
                if witness.order() == An_ref.order():
                    h1 = True
                    An = witness
    except Exception:
        h1 = False

    try:
        if h1 and An is not None:
            commutator = An.derived_subgroup()
            neg_q = (commutator.order() != An.order())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is an alternating group A_n (or an integer n >= 1 representing A_n)",
    "¬Q: The commutator subgroup of A_n is not equal to A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1