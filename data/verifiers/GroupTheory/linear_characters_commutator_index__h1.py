import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    try:
        # H_1: G' is the commutator subgroup of G
        # This is a definitional hypothesis. We verify that the witness is a valid group
        # by checking if it supports the computation of abelian invariants.
        if hasattr(witness, "abelian_invariants"):
            invs = witness.abelian_invariants()
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, "abelian_invariants"):
            invs = witness.abelian_invariants()
            # The index [G : G'] is the size of the abelianization G/G'.
            # For finitely generated groups, G/G' is isomorphic to Z^r x T.
            # If 0 is in the invariants, r > 0, so the abelianization is infinite.
            # In this case, [G : G'] is countably infinite (aleph_0),
            # but the number of degree-one characters (Hom(G/G', C^*)) is continuum (2^aleph_0).
            # Since aleph_0 != 2^aleph_0, the conclusion fails.
            neg_q = (0 in invs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G prime is the commutator subgroup of G",
    "¬Q: The number of distinct degree-one complex irreducible characters of G is not equal to the index of G prime"
]

N_HYP = 1
NEG_Q_INDEX = 1