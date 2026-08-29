import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G has exactly three distinct conjugacy classes
    try:
        h1 = False
        if hasattr(witness, "conjugacy_classes"):
            cc = witness.conjugacy_classes
            classes = cc() if callable(cc) else cc
            h1 = (len(classes) == 3)
    except Exception:
        h1 = False

    # neg_Q: G is not isomorphic to Z3 or S3
    try:
        is_Z3 = False
        is_S3 = False
        
        if hasattr(witness, "is_isomorphic"):
            try:
                is_Z3 = bool(witness.is_isomorphic(Z3))
            except Exception:
                pass
            try:
                is_S3 = bool(witness.is_isomorphic(S3))
            except Exception:
                pass
                
        # Fallback if is_isomorphic is not implemented but order is known
        if not is_Z3 and not is_S3 and hasattr(witness, "order"):
            try:
                ord_G = witness.order() if callable(witness.order) else witness.order
                if ord_G == 3:
                    is_Z3 = True
                elif ord_G == 6 and h1:
                    is_S3 = True
            except Exception:
                pass

        neg_q = not (is_Z3 or is_S3)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has exactly three distinct conjugacy classes",
    "¬Q: G is not isomorphic to Z3 or S3"
]

N_HYP = 1
NEG_Q_INDEX = 1