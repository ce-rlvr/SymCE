import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects for witness expressions
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
    # H_1: H is a subgroup of F such that H is equal to its commutator subgroup
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            H, F = witness
            # Check if H is a subgroup of F by verifying all generators of H are in F
            h_is_subgroup = all(g in F for g in H.generators)
        else:
            H = witness
            h_is_subgroup = True  # F is implicitly H itself
            
        H_derived = H.derived_subgroup()
        h1_ok = bool(h_is_subgroup and H.order() == H_derived.order())
    except Exception:
        h1_ok = False

    # ¬Q: H is not the trivial group
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            H, F = witness
        else:
            H = witness
            
        neg_q_ok = bool(H.order() > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of F such that H is equal to its commutator subgroup",
    "¬Q: H is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1