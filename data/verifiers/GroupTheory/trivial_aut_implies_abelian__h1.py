import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # H_1: The automorphism group Aut(G) is the trivial group.
        # Mathematically, a group has a trivial automorphism group if and only if 
        # it is the trivial group or the cyclic group of order 2.
        h1 = bool(witness.order() <= 2)
    except Exception:
        h1 = False

    try:
        # ¬Q: G is NOT an abelian group.
        neg_q = not bool(witness.is_abelian)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The automorphism group Aut(G) is the trivial group",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1