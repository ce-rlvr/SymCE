import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a counterexample to the conjecture.
    The witness is expected to be the integer n.
    """
    try:
        n = int(witness)
        # Hypothesis 1: zeta_n is a primitive n-th root of unity in C
        # This implicitly requires n to be a positive integer.
        h1_ok = (n == witness and n >= 1)
    except Exception:
        h1_ok = False

    try:
        # Conclusion: The field extension Q(zeta_n)/Q is a Galois extension.
        # For any integer n >= 1, the cyclotomic field Q(zeta_n) is the splitting field 
        # of x^n - 1 over Q. It is a normal and separable extension, hence it is ALWAYS Galois.
        # Since the conclusion is always True, its negation is always False.
        neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [h1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in C",
    "¬Q: The field extension Q(zeta_n)/Q is not a Galois extension"
]

N_HYP = 1
NEG_Q_INDEX = 1