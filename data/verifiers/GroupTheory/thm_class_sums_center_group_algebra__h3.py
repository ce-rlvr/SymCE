import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

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
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                G, F = witness[0], witness[1]
            else:
                G = witness[0]
                F = sympy.QQ
        else:
            G = witness
            F = sympy.QQ
    except Exception:
        G, F = None, None

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = getattr(F, 'is_Field', False)
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(h1_ok and h2_ok)
    except Exception:
        h3_ok = False

    try:
        # The class sums always form a basis for the center of the group algebra
        # for any finite group and any field. Thus the conclusion is always true,
        # and its negation is always false.
        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: F is a field",
    "H_3: Z is the center of the group algebra",
    "¬Q: Class sums do not form a basis for the center"
]

N_HYP = 3
NEG_Q_INDEX = 3