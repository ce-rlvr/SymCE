import sympy
from sympy import oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(G):
    try:
        if hasattr(G, 'order'):
            if callable(G.order):
                return G.order()
            else:
                return G.order
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    A = B = W = None
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            W = witness.get('W')
        elif hasattr(witness, 'A') and hasattr(witness, 'B'):
            A = witness.A
            B = witness.B
            W = getattr(witness, 'W', witness)
        else:
            A, B, W = witness
    except Exception:
        pass

    # H_1: A is a non-trivial group
    try:
        h1 = False
        if A is not None:
            order = get_order(A)
            if order is not None:
                h1 = bool(order > 1)
            elif hasattr(A, 'is_trivial'):
                is_triv = A.is_trivial() if callable(A.is_trivial) else A.is_trivial
                h1 = not bool(is_triv)
    except Exception:
        h1 = False

    # H_2: B is an infinite group
    try:
        h2 = False
        if B is not None:
            order = get_order(B)
            if order is not None:
                h2 = (order == oo or order == math.inf or str(order) == 'oo')
            elif hasattr(B, 'is_finite'):
                is_fin = B.is_finite() if callable(B.is_finite) else B.is_finite
                h2 = not bool(is_fin)
    except Exception:
        h2 = False

    # ¬Q: The center of W is not the trivial subgroup
    try:
        neg_q = False
        if W is not None:
            if hasattr(W, 'center'):
                center = W.center() if callable(W.center) else W.center
                c_order = get_order(center)
                if c_order is not None:
                    neg_q = bool(c_order > 1)
                elif hasattr(center, 'is_trivial'):
                    is_triv = center.is_trivial() if callable(center.is_trivial) else center.is_trivial
                    neg_q = not bool(is_triv)
                elif isinstance(center, (list, set, tuple)):
                    neg_q = len(center) > 1
            elif hasattr(W, 'has_trivial_center'):
                has_triv = W.has_trivial_center() if callable(W.has_trivial_center) else W.has_trivial_center
                neg_q = not bool(has_triv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a non-trivial group",
    "H_2: B is an infinite group",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2