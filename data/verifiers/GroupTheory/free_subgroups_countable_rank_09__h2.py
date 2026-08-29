import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

try:
    from sympy.combinatorics import FreeGroup
    F1 = FreeGroup('x')
    F2 = FreeGroup('x, y')
except ImportError:
    F1 = None
    F2 = None

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
    h1 = False
    neg_q = False
    
    try:
        if type(witness).__name__ == 'FreeGroup':
            h1 = True
            rank = len(witness.generators)
            neg_q = rank < 2
        elif type(witness).__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                h1 = True
                rank = len(witness.generators)
                neg_q = rank < 2
        elif hasattr(witness, 'is_trivial') and witness.is_trivial:
            h1 = True
            rank = 0
            neg_q = True
        elif isinstance(witness, int) and witness >= 0:
            h1 = True
            rank = witness
            neg_q = rank < 2
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F does not contain a subgroup isomorphic to the free group of countably infinite rank"
]

N_HYP = 1
NEG_Q_INDEX = 1