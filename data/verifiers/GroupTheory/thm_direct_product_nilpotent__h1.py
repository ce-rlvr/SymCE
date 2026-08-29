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

def _is_nilpotent(grp):
    val = grp.is_nilpotent
    if callable(val):
        return bool(val())
    return bool(val)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        else:
            G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = _is_nilpotent(H)
    except Exception:
        h1 = False
        
    try:
        try:
            prod = G * H
            neg_q = not _is_nilpotent(prod)
        except Exception:
            # For finite groups, G x H is nilpotent iff both G and H are nilpotent.
            neg_q = not (_is_nilpotent(G) and _is_nilpotent(H))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a nilpotent group",
    "¬Q: The direct product G x H is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1