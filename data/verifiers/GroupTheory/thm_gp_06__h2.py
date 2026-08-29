import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Set

# Top-level setup
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

def is_set(obj):
    return isinstance(obj, (set, frozenset, list, tuple, dict)) or isinstance(obj, Set)

def get_card(S):
    if isinstance(S, (set, frozenset, list, tuple, dict)):
        return len(S)
    if isinstance(S, Set):
        return S.cardinality
    return len(S)

def conditions(witness) -> list[bool]:
    try:
        X, Y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: Let X and Y be sets.
    try:
        h1 = bool(is_set(X) and is_set(Y))
    except Exception:
        h1 = False

    # H_2: The groups F(X) and F(Y) are isomorphic.
    # For free groups on sets X and Y, F(X) is isomorphic to F(Y) if and only if |X| == |Y|.
    try:
        h2 = bool(get_card(X) == get_card(Y))
    except Exception:
        h2 = False

    # ¬Q: The sets X and Y do not have the same cardinality.
    try:
        neg_q = bool(get_card(X) != get_card(Y))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are sets",
    "H_2: The groups F(X) and F(Y) are isomorphic",
    "¬Q: The sets X and Y do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2