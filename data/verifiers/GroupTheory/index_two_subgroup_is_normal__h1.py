import sympy
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture.
    The witness should be a tuple (G, H) where G and H are permutation groups.
    """
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1_ok = bool(H.is_subgroup(G))
    except Exception:
        h1_ok = False

    # H_2: The index of H in G is exactly 2
    try:
        h2_ok = bool(G.order() == 2 * H.order())
    except Exception:
        h2_ok = False

    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q_ok = not bool(H.is_normal(G))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is exactly 2",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2