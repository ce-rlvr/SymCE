import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import isprime

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
    # H_1: G has no proper non-trivial subgroups
    try:
        order = witness.order()
        # By Lagrange's and Cauchy's theorems, a finite group has no proper non-trivial 
        # subgroups if and only if its order is 1 or a prime number.
        h1 = (order == 1) or isprime(order)
    except Exception:
        h1 = False

    # ¬Q: G is NOT (either the trivial group or a cyclic group of prime order)
    try:
        order = witness.order()
        # Any group of prime order is cyclic. Thus, the conclusion holds iff order is 1 or prime.
        q = (order == 1) or isprime(order)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has no proper non-trivial subgroups",
    "¬Q: G is neither the trivial group nor a cyclic group of prime order"
]

N_HYP = 1
NEG_Q_INDEX = 1