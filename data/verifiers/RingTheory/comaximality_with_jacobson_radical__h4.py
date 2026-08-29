import sympy
from sympy import Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
from functools import reduce

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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # 1. Try to interpret witness as a tuple (R, I) where I is a SymPy ideal
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(I, 'ring') and hasattr(I, 'contains'):
                h1 = True
                h2 = True
                h3 = True
                neg_q = not bool(I.contains(I.ring.one))
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Try to interpret witness as a SymPy ideal directly
    try:
        if hasattr(witness, 'ring') and hasattr(witness, 'contains'):
            h1 = True
            h2 = True
            h3 = True
            neg_q = not bool(witness.contains(witness.ring.one))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 3. Try to interpret witness as a list of integer generators for an ideal in Z
    try:
        if isinstance(witness, (list, tuple)) and all(isinstance(x, (int, Integer)) for x in witness):
            if len(witness) > 0:
                n = reduce(math.gcd, [int(x) for x in witness])
            else:
                n = 0
            h1 = True
            h2 = True
            h3 = True
            neg_q = (abs(n) != 1)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 4. Try to interpret witness as a single integer generator for an ideal in Z
    try:
        n = int(witness)
        h1 = True
        h2 = True
        h3 = True
        neg_q = (abs(n) != 1)
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: J(R) is the Jacobson radical of R",
    "H_3: I is an ideal of R",
    "¬Q: I is not the entire ring R"
]

N_HYP = 3
NEG_Q_INDEX = 3