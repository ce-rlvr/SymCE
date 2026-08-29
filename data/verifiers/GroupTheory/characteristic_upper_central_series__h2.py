import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: Z_i(G) is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (a group G, or a tuple containing G),
    check if it satisfies the hypotheses and fails the conclusion.
    """
    try:
        # Extract the group if the witness is a tuple (e.g., (G, i))
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
            
        h1_ok = bool(G.is_nilpotent)
    except Exception:
        h1_ok = False

    # The terms of the upper central series Z_i(G) are ALWAYS characteristic subgroups 
    # of G for any group G. This is a fundamental theorem of group theory.
    # Because the conclusion "Z_i(G) is a characteristic subgroup of G" is unconditionally true,
    # its negation is unconditionally false.
    neg_q_ok = False

    return [h1_ok, neg_q_ok]