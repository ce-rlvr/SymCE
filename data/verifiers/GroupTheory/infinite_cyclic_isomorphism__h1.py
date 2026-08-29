import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is cyclic",
    "H_2: G is infinite",
    "¬Q: G is not isomorphic to the additive group of integers"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1: G is cyclic
    h1 = False
    try:
        if hasattr(witness, 'is_cyclic'):
            val = witness.is_cyclic
            if callable(val):
                h1 = bool(val())
            elif val is not None:
                h1 = bool(val)
        else:
            class_name = witness.__class__.__name__
            if class_name in ('FreeGroup', 'FpGroup'):
                h1 = len(witness.generators) <= 1
            elif hasattr(witness, 'generators'):
                h1 = len(witness.generators) <= 1
    except Exception:
        h1 = False

    # H_2: G is infinite
    h2 = False
    try:
        class_name = witness.__class__.__name__
        if class_name == 'FreeGroup':
            h2 = len(witness.generators) > 0
        elif class_name == 'FpGroup' and hasattr(witness, 'relators') and len(witness.relators) == 0:
            h2 = len(witness.generators) > 0
        elif hasattr(witness, 'order'):
            val = witness.order
            if callable(val):
                val = val()
            if val == sympy.oo:
                h2 = True
        elif hasattr(witness, 'is_finite'):
            val = witness.is_finite
            if callable(val):
                val = val()
            if val is False:
                h2 = True
        elif hasattr(witness, 'is_infinite'):
            val = witness.is_infinite
            if callable(val):
                val = val()
            if val is True:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is not isomorphic to Z
    neg_q = False
    try:
        is_grp = False
        class_name = witness.__class__.__name__
        if isinstance(witness, PermutationGroup) or class_name in ('FpGroup', 'FreeGroup'):
            is_grp = True
        elif hasattr(witness, 'is_group') and witness.is_group:
            is_grp = True
        elif hasattr(witness, 'generators') and hasattr(witness, 'identity'):
            is_grp = True
        
        # In group theory, any infinite cyclic group is isomorphic to Z.
        # If the witness is a group, it is isomorphic to Z iff it is infinite and cyclic.
        # If the witness is not a group, it cannot be isomorphic to the group Z.
        if is_grp:
            is_iso = h1 and h2
        else:
            is_iso = False
            
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]