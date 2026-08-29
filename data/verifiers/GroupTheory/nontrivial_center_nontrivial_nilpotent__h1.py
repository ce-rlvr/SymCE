import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
    # H_1: G is not the trivial group
    try:
        h1_ok = bool(witness.order() > 1)
    except Exception:
        h1_ok = False

    # ¬Q: The center Z(G) is the trivial group
    try:
        try:
            c = witness.center()
            if hasattr(c, 'order'):
                neg_q_ok = bool(c.order() == 1)
            else:
                neg_q_ok = bool(len(c) == 1)
        except Exception:
            # Fallback for groups where .center() might not be implemented
            gens = witness.generators
            c_count = 0
            for g in witness.elements:
                if all(g * gen == gen * g for gen in gens):
                    c_count += 1
            neg_q_ok = bool(c_count == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "¬Q: The center Z(G) is the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1