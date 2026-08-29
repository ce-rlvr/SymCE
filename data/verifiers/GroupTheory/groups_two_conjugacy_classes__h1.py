import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    # H_1: G has exactly two conjugacy classes
    try:
        if hasattr(witness, 'conjugacy_classes'):
            classes = witness.conjugacy_classes()
            h1 = len(list(classes)) == 2
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: G is not isomorphic to the cyclic group of order 2
    try:
        evaluated = False
        neg_q = False
        
        if hasattr(witness, 'is_isomorphic'):
            try:
                neg_q = not witness.is_isomorphic(Z2)
                evaluated = True
            except Exception:
                pass
        
        if not evaluated and hasattr(witness, 'order'):
            try:
                # Z2 is the unique group of order 2 up to isomorphism
                neg_q = witness.order() != 2
                evaluated = True
            except Exception:
                pass
                
        if not evaluated:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has exactly two conjugacy classes",
    "¬Q: G is not isomorphic to the cyclic group of order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1