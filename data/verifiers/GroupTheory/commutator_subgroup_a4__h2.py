import sympy
from sympy.combinatorics.named_groups import AlternatingGroup, AbelianGroup

# Top-level setup
A4 = AlternatingGroup(4)
# V4 is the Klein four-group, which is isomorphic to Z2 x Z2
V4 = AbelianGroup(2, 2)

def conditions(witness) -> list[bool]:
    # H_1: Let A_4 be the alternating group on 4 letters
    # We interpret this as the witness being isomorphic to A_4
    try:
        h1 = bool(witness.is_isomorphic(A4))
    except Exception:
        h1 = False

    # Conclusion: The commutator subgroup of A_4 is exactly V_4
    # We evaluate this on the witness
    try:
        der = witness.derived_subgroup()
        q = der.is_isomorphic(V4)
        neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is isomorphic to the alternating group A_4",
    "¬Q: The commutator subgroup of the witness is not exactly V_4"
]

N_HYP = 1
NEG_Q_INDEX = 1