import sympy
from sympy.combinatorics import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    Checks whether the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: Let n be an integer with n >= 5
    try:
        n = int(witness)
        h1 = (n == witness) and (n >= 5)
    except Exception:
        h1 = False

    # ¬Q: The commutator subgroup of A_n is NOT equal to A_n
    try:
        n = int(witness)
        if n != witness or n < 1:
            neg_q = False
        else:
            G = AlternatingGroup(n)
            D = G.derived_subgroup()
            neg_q = (D.order() != G.order())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 5",
    "¬Q: The commutator subgroup of A_n is not equal to A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1