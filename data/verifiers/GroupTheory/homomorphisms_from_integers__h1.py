import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    try:
        # The hypothesis implicitly requires that G is a group.
        # We check for standard group attributes in SymPy.
        h1 = hasattr(witness, 'is_abelian') and hasattr(witness, 'generators')
    except Exception:
        h1 = False

    try:
        # The conclusion states that Hom(Z, G) is isomorphic to G.
        # For Hom(Z, G) to be a group under pointwise multiplication (and isomorphic to G),
        # G must be an abelian group. If G is non-abelian, Hom(Z, G) is not a group,
        # hence cannot be isomorphic to G.
        # Therefore, the conclusion fails (neg_Q is True) exactly when G is non-abelian.
        neg_q = bool(not witness.is_abelian)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Hom(Z, G) is the group of all group homomorphisms from Z to G (G is a group)",
    "¬Q: Hom(Z, G) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1