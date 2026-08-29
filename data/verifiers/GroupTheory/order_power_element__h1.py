import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

class CustomElement:
    """
    A helper class for constructing custom algebraic elements.
    Useful for creating counterexamples in non-group structures.
    """
    def __init__(self, order_val, pow_func):
        self._order = order_val
        self._pow_func = pow_func
        
    def order(self):
        return self._order
        
    def __pow__(self, k):
        return self._pow_func(self, k)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            g = witness.get('g')
            k = witness.get('k')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                g, k = witness
            elif len(witness) == 3:
                g, _, k = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: g is an element of G
    h1 = (g is not None)
    
    # H_2: the order of g is a finite integer n
    try:
        if callable(getattr(g, 'order', None)):
            n = g.order()
        else:
            n = g.order
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
        n = int(n)
    except Exception:
        h2 = False
        n = None
        
    # H_3: k is an integer
    try:
        h3 = isinstance(k, (int, sympy.Integer)) and not isinstance(k, bool)
        k = int(k)
    except Exception:
        h3 = False
        
    # ¬Q: The order of the element g^k is not n / gcd(n, k)
    try:
        if h2 and h3:
            gk = g ** k
            if callable(getattr(gk, 'order', None)):
                order_gk = gk.order()
            else:
                order_gk = gk.order
            order_gk = int(order_gk)
            
            expected = n // math.gcd(n, k)
            neg_q = (order_gk != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "H_2: the order of g is a finite integer n",
    "H_3: k is an integer",
    "¬Q: The order of the element g^k is not n / gcd(n, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3