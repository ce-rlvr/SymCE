import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
from sympy import gcd

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            n = witness.get('n')
            k = witness.get('k')
        else:
            G, g, n, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'is_group') or hasattr(G, 'elements')
    except Exception:
        h1 = False

    # H_2: g is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(g))
        elif hasattr(G, 'elements'):
            h2 = g in G.elements
        else:
            h2 = g in G
    except Exception:
        h2 = False

    # H_3: the order of g is a finite integer n
    try:
        if hasattr(g, 'order'):
            order_g = g.order()
        elif hasattr(g, 'is_Matrix') and g.is_Matrix:
            order_g = None
            ident = sympy.eye(g.shape[0])
            curr = g
            for i in range(1, int(n) + 2):
                if curr == ident:
                    order_g = i
                    break
                curr = curr * g
        else:
            order_g = g.order()
            
        h3 = isinstance(n, (int, sympy.Integer)) and n > 0 and order_g == n
    except Exception:
        h3 = False

    # ¬Q: The order of the element g^k is not n / gcd(n, k)
    try:
        expected = n / gcd(n, k)
        gk = g**k
        
        if hasattr(gk, 'order'):
            order_gk = gk.order()
        elif hasattr(gk, 'is_Matrix') and gk.is_Matrix:
            order_gk = None
            ident = sympy.eye(gk.shape[0])
            curr = gk
            max_iter = int(max(n, expected)) + 2
            for i in range(1, max_iter):
                if curr == ident:
                    order_gk = i
                    break
                curr = curr * gk
            if order_gk is None:
                raise ValueError("Order not found within limits")
        else:
            order_gk = gk.order()
            
        q = (order_gk == expected)
        neg_q = not q
    except Exception:
        # If any operation (like g**k or gcd) fails, the conclusion formula is invalid, so it fails.
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: the order of g is a finite integer n",
    "¬Q: The order of the element g^k is not n / gcd(n, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3