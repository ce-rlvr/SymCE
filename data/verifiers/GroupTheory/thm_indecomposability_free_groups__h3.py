import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        F, A, B = witness
    except Exception:
        return [False, False, False]

    # H1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # Helper to parse subgroups provided as FreeGroup, single element, or iterable of elements
    try:
        def parse_subgroup(S):
            if type(S).__name__ == 'FreeGroup':
                return list(S.generators)
            if hasattr(S, 'group'):
                return [S]
            if isinstance(S, (list, set, tuple)):
                return list(S)
            return None

        A_list = parse_subgroup(A)
        B_list = parse_subgroup(B)

        if A_list is None or B_list is None:
            h2 = False
        else:
            # H2: A and B are subgroups of F (their generators must belong to F)
            h2_A = all(hasattr(x, 'group') and x.group == F for x in A_list)
            h2_B = all(hasattr(x, 'group') and x.group == F for x in B_list)
            h2 = h1 and h2_A and h2_B
    except Exception:
        h2 = False
        A_list = None
        B_list = None

    # neg_Q: A is not trivial AND B is not trivial
    try:
        if A_list is None or B_list is None:
            neg_q = False
        else:
            # A subgroup is trivial if all its generators evaluate to the identity
            A_trivial = all(x == F.identity for x in A_list)
            B_trivial = all(x == F.identity for x in B_list)
            neg_q = (not A_trivial) and (not B_trivial)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: A and B are subgroups of F",
    "¬Q: A is not trivial and B is not trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2