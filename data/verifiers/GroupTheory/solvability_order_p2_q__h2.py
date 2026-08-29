import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
        order = witness.order()
        factors = factorint(order)
        # Check if the order is exactly p^2 * q for distinct primes p and q
        h1 = (len(factors) == 2 and sorted(list(factors.values())) == [1, 2])
    except Exception:
        h1 = False

    try:
        # The conclusion is that G is solvable, so its negation is that G is NOT solvable
        neg_q = not witness.is_solvable
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has order p^2 q for distinct primes p and q",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1