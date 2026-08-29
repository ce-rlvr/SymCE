import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if len(witness) != 2:
            return [False, False, False]
        G, V_obj = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite cyclic group
    try:
        h1 = False
        order_attr = getattr(G, 'order', None)
        order = order_attr() if callable(order_attr) else order_attr
        
        elements_attr = getattr(G, 'elements', None)
        elements = elements_attr() if callable(elements_attr) else elements_attr
        
        if order is not None and elements is not None:
            # A finite group is cyclic if it has an element of order equal to the group's order
            for g in elements:
                g_order_attr = getattr(g, 'order', None)
                g_order = g_order_attr() if callable(g_order_attr) else g_order_attr
                if g_order == order:
                    h1 = True
                    break
    except Exception:
        h1 = False

    # H_2: V is a finite-dimensional vector space over the complex numbers C
    try:
        h2 = False
        dim = None
        if isinstance(V_obj, int):
            if V_obj >= 0:
                h2 = True
                dim = V_obj
        elif hasattr(V_obj, 'shape') and len(V_obj.shape) == 2:
            if V_obj.shape[0] == V_obj.shape[1]:
                h2 = True
                dim = V_obj.shape[0]
        elif isinstance(V_obj, (list, tuple)) and len(V_obj) > 0 and hasattr(V_obj[0], 'shape'):
            if len(V_obj[0].shape) == 2 and V_obj[0].shape[0] == V_obj[0].shape[1]:
                h2 = True
                dim = V_obj[0].shape[0]
        elif isinstance(V_obj, dict) and len(V_obj) > 0:
            first_val = next(iter(V_obj.values()))
            if hasattr(first_val, 'shape') and len(first_val.shape) == 2 and first_val.shape[0] == first_val.shape[1]:
                h2 = True
                dim = first_val.shape[0]
    except Exception:
        h2 = False

    # neg_Q: The dimension of V is not exactly 1
    try:
        neg_q = False
        if dim is not None:
            neg_q = (dim != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: V is a finite-dimensional vector space over the complex numbers C",
    "¬Q: The dimension of V is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2