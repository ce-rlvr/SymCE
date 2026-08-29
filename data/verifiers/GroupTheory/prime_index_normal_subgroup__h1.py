import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        # H_1: G is not the trivial group
        h1 = bool(witness.order() > 1)
    except Exception:
        h1 = False

    try:
        # ¬Q: G does NOT contain a normal subgroup of prime index
        # 
        # Mathematical justification:
        # A finite group G has a normal subgroup of prime index p if and only if 
        # its abelianization G/G' has a subgroup of index p, which happens iff 
        # G/G' is non-trivial (i.e., G is not perfect).
        # Therefore, G fails to have a normal subgroup of prime index if and only if 
        # G is perfect, meaning G is equal to its derived subgroup G'.
        G_prime = witness.derived_subgroup()
        neg_q = bool(witness.order() == G_prime.order())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "¬Q: G does not contain a normal subgroup of prime index"
]

N_HYP = 1
NEG_Q_INDEX = 1