import sympy
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, m = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: Let G be a cyclic group.
    try:
        h1 = bool(G.is_cyclic)
    except Exception:
        h1 = False
        
    # H_2: Let the order of G be a finite integer n.
    try:
        n = G.order()
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h2 = False
        
    # H_3: Let m be an integer.
    try:
        h3 = isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool)
    except Exception:
        h3 = False
        
    # neg_Q: The number of elements x in G satisfying x^m = e is NOT exactly gcd(m,n).
    try:
        n_val = int(G.order())
        m_val = int(m)
        expected = math.gcd(m_val, n_val)
        
        # Prevent timeout for excessively large groups
        if n_val > 5000:
            neg_q = False
        else:
            count = 0
            for x in G.elements:
                if x**m_val == G.identity:
                    count += 1
            neg_q = (count != expected)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: The order of G is a finite integer n",
    "H_3: m is an integer",
    "¬Q: The number of elements x in G satisfying x^m = e is not exactly gcd(m,n)"
]

N_HYP = 3
NEG_Q_INDEX = 3