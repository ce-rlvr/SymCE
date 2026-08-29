import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        # The witness can be a tuple (G, x) or just G.
        # If just G is provided, we default x to the identity element.
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G = witness
            x = G.identity if hasattr(G, 'identity') else None
    except Exception:
        return [False, False]

    # H_1: G is a finite abelian group, written additively
    try:
        h1 = bool(getattr(G, 'is_abelian', False))
        if h1:
            # Ensure it's finite by trying to list its elements
            _ = list(G.elements)
    except Exception:
        h1 = False

    # neg_Q: The sum of all elements in G is not equal to x
    try:
        elements = list(G.elements)
        total = G.identity
        # Since the group is abelian, the order of multiplication (addition) does not matter
        for e in elements:
            total = total * e
        neg_q = bool(total != x)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group, written additively",
    "¬Q: The sum of all elements in G is not equal to x"
]

N_HYP = 1
NEG_Q_INDEX = 1