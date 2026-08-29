import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G, H) or a dictionary {'G': G, 'H': H}.
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
    else:
        try:
            G, H = witness
        except Exception:
            return [False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: It is NOT the case that (G x H is solvable iff both G and H are solvable)
    try:
        # Check if the direct product G x H is solvable
        try:
            prod = G * H
            prod_solvable = bool(prod.is_solvable)
        except Exception:
            prod_solvable = False

        # Check if both G and H are solvable
        try:
            both_solvable = bool(G.is_solvable and H.is_solvable)
        except Exception:
            both_solvable = False

        # The conclusion is (prod_solvable == both_solvable)
        # We want the negation of the conclusion
        neg_q_ok = (prod_solvable != both_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: It is not the case that G x H is solvable iff both G and H are solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1