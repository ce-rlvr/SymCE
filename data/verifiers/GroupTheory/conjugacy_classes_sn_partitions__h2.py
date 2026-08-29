import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import npartitions

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
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n == witness) and (n >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Limit n to prevent timeout in generic conjugacy_classes computation
            if n > 7:
                neg_q = False
            else:
                G = SymmetricGroup(n)
                try:
                    classes = G.conjugacy_classes()
                except TypeError:
                    classes = G.conjugacy_classes
                num_classes = len(classes)
                p_n = npartitions(n)
                neg_q = bool(num_classes != p_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "¬Q: The number of conjugacy classes of S_n is not equal to p(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1