import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: The order of G is an odd integer
        order = witness.order()
        h1 = (int(order) % 2 == 1)
    except Exception:
        h1 = False

    try:
        # ¬Q: The map f(x) = x^2 is not a bijection
        # For a finite group, the map is a bijection iff it is surjective.
        elements = list(witness.generate())
        squares = set()
        for x in elements:
            squares.add(x**2)
        neg_q = len(squares) != len(elements)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an odd integer",
    "¬Q: The map f(x) = x^2 is not a bijection"
]

N_HYP = 1
NEG_Q_INDEX = 1