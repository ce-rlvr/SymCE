import sympy
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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(H.is_abelian)
    except Exception:
        h1_ok = False
        
    try:
        # The direct product G x H is abelian iff both G and H are abelian.
        # The conclusion is that G x H is abelian.
        # The negated conclusion is that G x H is NOT abelian.
        neg_q_ok = not (bool(G.is_abelian) and bool(H.is_abelian))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is an abelian group",
    "¬Q: The direct product G x H is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1