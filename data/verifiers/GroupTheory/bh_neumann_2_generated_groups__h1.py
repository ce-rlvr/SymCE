import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        # The conclusion is that the cardinality of S is uncountably infinite.
        # The negated conclusion is that S is NOT uncountably infinite (i.e., it is finite or countably infinite).
        from sympy import Set
        if isinstance(witness, Set):
            # In SymPy, is_countable is False for uncountably infinite sets (like Reals).
            if witness.is_countable is False:
                neg_q = False
            else:
                neg_q = True
        else:
            # Standard Python collections (lists, tuples, sets, dicts), numbers, and finite groups
            # are all finite or at most countably infinite.
            neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The cardinality of S is not uncountably infinite"
]

N_HYP = 0
NEG_Q_INDEX = 0