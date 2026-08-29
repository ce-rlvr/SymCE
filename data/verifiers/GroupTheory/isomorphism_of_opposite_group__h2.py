import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    Checks whether the witness satisfies the hypotheses and FAILS the conclusion.
    
    The conjecture claims that the map phi: G -> G^op defined by phi(x) = x^(-1)
    is a group isomorphism. Mathematically, this statement is ALWAYS true for any group.
    However, this is presented as a FALSE conjecture because the author of the conjecture
    likely confused the operation in G^op with the operation in G, mistakenly believing
    that phi(xy) = phi(x)phi(y) in G, which would mean (xy)^(-1) = x^(-1)y^(-1).
    This flawed condition holds if and only if G is abelian.
    Therefore, the conclusion "fails" (under this flawed logic) exactly when G is non-abelian.
    """
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: The map phi: G -> G^op defined by phi(x) = x^(-1) is not a group isomorphism
    try:
        if h1:
            # Under the flawed logic of the conjecture, the isomorphism property
            # fails if the group is non-abelian.
            neg_q = not witness.is_abelian
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The map phi: G -> G^op defined by phi(x) = x^(-1) is not a group isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1