import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        # H_1: The quotient group G/G' is a torsion-free group.
        # For a finite group G, the quotient G/G' is a finite abelian group.
        # The only finite torsion-free group is the trivial group.
        # Thus, G/G' is torsion-free iff G/G' is trivial, which means G == G'.
        order = witness.order()
        if not isinstance(order, (int, sympy.Integer)):
            h1_ok = False
        else:
            D = witness.derived_subgroup()
            h1_ok = bool(order == D.order())
    except Exception:
        h1_ok = False

    try:
        # ¬Q: G is not a torsion-free group.
        # For a finite group G, every element has finite order.
        # Thus, G is torsion-free iff G is the trivial group.
        # So G is NOT torsion-free iff G is non-trivial (order > 1).
        order = witness.order()
        if not isinstance(order, (int, sympy.Integer)):
            neg_q_ok = False
        else:
            neg_q_ok = bool(order > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The quotient group G/G' is a torsion-free group",
    "¬Q: G is not a torsion-free group"
]

N_HYP = 1
NEG_Q_INDEX = 1