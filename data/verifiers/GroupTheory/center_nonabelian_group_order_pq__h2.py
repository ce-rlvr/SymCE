import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness):
    G, p, q = None, None, None
    
    # Unpack witness if it's a tuple (e.g., (G, p, q))
    if isinstance(witness, tuple):
        for item in witness:
            if hasattr(item, 'is_abelian'):
                G = item
            elif p is None:
                p = item
            else:
                q = item
    else:
        G = witness

    # If p and q are not provided, try to infer them from the order of G
    if p is None or q is None:
        try:
            order_attr = getattr(G, 'order')
            order = order_attr() if callable(order_attr) else order_attr
            factors = sympy.ntheory.factorint(order)
            if len(factors) == 2 and all(v == 1 for v in factors.values()):
                p, q = list(factors.keys())
            else:
                p, q = 1, order
        except Exception:
            p, q = 1, 1

    # H_1: p and q are distinct prime numbers
    try:
        h1 = sympy.isprime(p) and sympy.isprime(q) and p != q
    except Exception:
        h1 = False

    # H_2: G is non-abelian
    try:
        is_ab = getattr(G, 'is_abelian')
        is_ab = is_ab() if callable(is_ab) else is_ab
        h2 = not bool(is_ab)
    except Exception:
        h2 = False

    # H_3: The order of G is pq
    try:
        order_attr = getattr(G, 'order')
        order = order_attr() if callable(order_attr) else order_attr
        h3 = order == p * q
    except Exception:
        h3 = False

    # ¬Q: The center Z(G) is not the trivial subgroup
    try:
        center_attr = getattr(G, 'center')
        center = center_attr() if callable(center_attr) else center_attr
        
        # Handle both cases: if center is a Subgroup object or a list of elements
        if hasattr(center, 'order'):
            center_order = center.order() if callable(center.order) else center.order
            neg_q = center_order > 1
        else:
            neg_q = len(center) > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: G is non-abelian",
    "H_3: The order of G is pq",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3