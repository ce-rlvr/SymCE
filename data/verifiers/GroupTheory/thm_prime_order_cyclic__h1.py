import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    # H_1: The order of G is a prime number p
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
        else:
            order = len(witness)
        h1 = bool(isprime(order))
    except Exception:
        h1 = False

    # ¬Q: G is not a cyclic group
    try:
        if hasattr(witness, 'is_cyclic'):
            if callable(witness.is_cyclic):
                is_cyclic = witness.is_cyclic()
            else:
                is_cyclic = witness.is_cyclic
            neg_q = not bool(is_cyclic)
        else:
            # If it lacks the property, it is not a cyclic group
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is a prime number p",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1