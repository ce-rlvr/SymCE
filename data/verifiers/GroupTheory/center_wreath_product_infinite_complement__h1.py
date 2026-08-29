import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Helper for infinite abelian groups (e.g., Z)
class _InfiniteAbelianGroup:
    @property
    def is_infinite(self):
        return True
    
    @property
    def is_abelian(self):
        return True
        
    def order(self):
        return sympy.oo
        
    def center(self):
        return self

Z_inf = _InfiniteAbelianGroup()

CONDITION_LABELS = [
    "H_1: B is an infinite group",
    "H_2: W is the restricted wreath product of A by B",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        A, B, W = witness
    except Exception:
        return [False, False, False]
        
    # H1: B is an infinite group
    try:
        h1 = False
        if hasattr(B, 'order'):
            order_val = B.order() if callable(B.order) else B.order
            if order_val == sympy.oo or order_val == math.inf:
                h1 = True
        if not h1 and hasattr(B, 'is_infinite'):
            is_inf = B.is_infinite() if callable(B.is_infinite) else B.is_infinite
            if is_inf:
                h1 = True
    except Exception:
        h1 = False

    # H2: W is the restricted wreath product of A by B
    try:
        h2 = False
        a_order = None
        if hasattr(A, 'order'):
            a_order = A.order() if callable(A.order) else A.order
            
        # If A is the trivial group, the restricted wreath product of A by B is isomorphic to B.
        if a_order == 1:
            h2 = (W is B) or (W == B)
        else:
            # Fallback for custom mock objects if A is not trivial
            if hasattr(W, 'is_wreath_product_of'):
                h2 = W.is_wreath_product_of(A, B)
    except Exception:
        h2 = False

    # neg_Q: The center of W is not the trivial subgroup
    try:
        neg_q = False
        w_order = None
        if hasattr(W, 'order'):
            w_order = W.order() if callable(W.order) else W.order
            
        w_is_abelian = False
        if hasattr(W, 'is_abelian'):
            w_is_abelian = W.is_abelian() if callable(W.is_abelian) else W.is_abelian
            
        # If W is abelian, its center is itself. If it's non-trivial, the center is non-trivial.
        if w_is_abelian:
            if w_order == sympy.oo or w_order == math.inf:
                neg_q = True
            elif isinstance(w_order, (int, sympy.Integer)) and w_order > 1:
                neg_q = True
        
        # Check explicit center if available
        if not neg_q and hasattr(W, 'center'):
            c = W.center() if callable(W.center) else W.center
            c_order = c.order() if callable(c.order) else getattr(c, 'order', None)
            if c_order is not None and c_order != 1:
                neg_q = True
                
        # Check explicit boolean flag if available
        if not neg_q and hasattr(W, 'center_is_trivial'):
            is_trivial = W.center_is_trivial() if callable(W.center_is_trivial) else W.center_is_trivial
            neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]