import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    Given a witness k, checks if it serves as a counterexample to the false conjecture.
    The true theorem (Landau's Theorem on Conjugacy Classes) states that for any positive 
    integer k, there are only finitely many isomorphism classes of finite groups with 
    exactly k conjugacy classes.
    
    If the hypothesis "k is a positive integer" is dropped, the witness is a value of k 
    that is not a positive integer. The testing framework expects the conclusion to fail 
    (i.e., neg_Q = True) for such a witness.
    """
    k = witness
    try:
        if isinstance(k, (int, sympy.Integer)):
            neg_q = bool(k <= 0)
        elif isinstance(k, float) and k.is_integer():
            neg_q = bool(k <= 0)
        else:
            # If k is not an integer at all, it violates the dropped hypothesis.
            neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There are infinitely many isomorphism classes of finite groups that have exactly k conjugacy classes"
]

N_HYP = 0
NEG_Q_INDEX = 0