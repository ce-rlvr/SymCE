import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: Let S_n be the symmetric group on n letters",
    "¬Q: Not every permutation in S_n can be expressed as a finite product of transpositions"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Check if witness is an integer n
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 0:
                h1 = True
                # For n < 2, there are no transpositions, so we cannot form a non-empty product.
                neg_q = (n < 2)
                return [h1, neg_q]
    except Exception:
        pass

    # Check if witness is a permutation group
    try:
        if not getattr(witness, 'is_group', False):
            h1 = False
        elif not hasattr(witness, 'degree') or not hasattr(witness, 'order'):
            h1 = False
        else:
            n = witness.degree
            # A permutation group of degree n is the symmetric group S_n iff its order is n!
            h1 = (witness.order() == math.factorial(n))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # In S_n, transpositions exist iff degree >= 2.
            # If degree < 2, the set of transpositions is empty, so the identity 
            # cannot be expressed as a non-empty product of transpositions.
            neg_q = (witness.degree < 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]