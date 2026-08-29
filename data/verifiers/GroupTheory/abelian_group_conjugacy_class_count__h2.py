import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    # H_1: G is a finite group
    try:
        # In SymPy, finite groups are typically represented as PermutationGroup
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: It is not the case that G is abelian if and only if k = |G|
    # (where k is the number of conjugacy classes)
    try:
        if callable(witness.conjugacy_classes):
            classes = witness.conjugacy_classes()
        else:
            classes = witness.conjugacy_classes
        k = len(classes)
        
        is_abelian = bool(witness.is_abelian)
        
        if callable(witness.order):
            order = int(witness.order())
        else:
            order = int(witness.order)
            
        # The conclusion is: G is abelian iff k == |G|
        conclusion = (is_abelian == (k == order))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: It is not the case that G is abelian if and only if k = |G|"
]

N_HYP = 1
NEG_Q_INDEX = 1