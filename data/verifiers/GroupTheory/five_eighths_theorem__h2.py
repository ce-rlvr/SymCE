import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.elements)
            order = len(elements)
            commuting_pairs = sum(1 for x in elements for y in elements if x * y == y * x)
            neg_q = (commuting_pairs * 8) > (5 * order ** 2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The number of commuting pairs in G x G is strictly greater than (5/8) * |G|^2"
]

N_HYP = 1
NEG_Q_INDEX = 1