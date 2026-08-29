import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, x, y, z = witness
    except Exception:
        return [False, False, False]

    # H_1: G is nilpotent of class at most 2
    try:
        h1 = bool(G.is_nilpotent and G.nilpotency_class <= 2)
    except Exception:
        h1 = False

    # H_2: Let x, y, and z be elements of G
    try:
        h2 = bool(x in G and y in G and z in G)
    except Exception:
        h2 = False

    # ¬Q: The conclusion must FAIL at the witness
    # Conclusion: commutator(xy, z) = commutator(x, z)commutator(y, z) and commutator(x, yz) = commutator(x, y)commutator(x, z)
    try:
        # Standard group-theoretic commutator: commutator(a, b) = a^-1 b^-1 a b
        def comm(a, b):
            return a**-1 * b**-1 * a * b

        xy = x * y
        yz = y * z

        eq1 = comm(xy, z) == comm(x, z) * comm(y, z)
        eq2 = comm(x, yz) == comm(x, y) * comm(x, z)

        neg_q = not (eq1 and eq2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is nilpotent of class at most 2",
    "H_2: x, y, and z are elements of G",
    "¬Q: comm(xy, z) != comm(x, z)comm(y, z) or comm(x, yz) != comm(x, y)comm(x, z)"
]

N_HYP = 2
NEG_Q_INDEX = 2