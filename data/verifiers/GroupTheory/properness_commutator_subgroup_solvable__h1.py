import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        w_order = witness.order() if callable(witness.order) else witness.order
        h1_ok = bool(w_order > 1)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(witness.is_solvable() if callable(witness.is_solvable) else witness.is_solvable)
    except Exception:
        h2_ok = False

    try:
        w_order = witness.order() if callable(witness.order) else witness.order
        derived = witness.derived_subgroup()
        d_order = derived.order() if callable(derived.order) else derived.order
        
        # The conclusion is that G' is a proper subgroup of G.
        # The negation is that G' is NOT a proper subgroup of G (i.e., G' == G).
        neg_q_ok = bool(d_order == w_order)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "H_2: G is a solvable group",
    "¬Q: The commutator subgroup G' is not a proper subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2