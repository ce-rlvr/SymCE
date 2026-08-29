import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    # H_1: The order of G is an odd integer
    try:
        order_attr = witness.order
        if callable(order_attr):
            order_val = order_attr()
        else:
            order_val = order_attr
        h1 = (int(order_val) % 2 == 1)
    except Exception:
        h1 = False

    # ¬Q: The number of conjugacy classes of G is an even integer (not odd)
    try:
        if hasattr(witness, 'is_abelian') and witness.is_abelian:
            order_attr = witness.order
            if callable(order_attr):
                order_val = order_attr()
            else:
                order_val = order_attr
            num_classes = int(order_val)
        else:
            classes_attr = witness.conjugacy_classes
            if callable(classes_attr):
                classes_val = classes_attr()
            else:
                classes_val = classes_attr
            num_classes = len(list(classes_val))
        
        neg_q = (num_classes % 2 == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an odd integer",
    "¬Q: The number of conjugacy classes of G is not an odd integer"
]

N_HYP = 1
NEG_Q_INDEX = 1