import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(H.is_subgroup(G))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(G.order() == 2 * H.order())
    except Exception:
        h2_ok = False

    try:
        G_prime = G.derived_subgroup()
        neg_q_ok = not bool(G_prime.is_subgroup(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is equal to 2",
    "¬Q: The commutator subgroup is not a subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2