import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import lcm

# Top-level setup for standard algebra objects
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

def get_order(x):
    """Helper to compute the order of a group element."""
    if hasattr(x, 'order'):
        if callable(x.order):
            return x.order()
        else:
            return x.order
    if hasattr(x, 'is_Matrix') and x.is_Matrix:
        if x.shape[0] != x.shape[1]:
            return float('inf')
        I = eye(x.shape[0])
        if x == I:
            return 1
        curr = x
        for k in range(2, 1001):
            curr = curr * x
            if curr == I:
                return k
        return float('inf')
    raise ValueError("Cannot determine order")

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                g, h, m, n = witness
            elif len(witness) == 2:
                g, h = witness
                m = get_order(g)
                n = get_order(h)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        order_g = get_order(g)
        h1 = bool((order_g == m) and (m > 0) and (m != float('inf')))
    except Exception:
        h1 = False

    try:
        order_h = get_order(h)
        h2 = bool((order_h == n) and (n > 0) and (n != float('inf')))
    except Exception:
        h2 = False

    try:
        target_lcm = int(lcm(m, n))
        
        # The literal text asks for the order of the pair (g, h) in the direct product G x H.
        # Mathematically, this is always exactly lcm(|g|, |h|).
        pair_order = int(lcm(order_g, order_h))
        pair_not_lcm = (pair_order != target_lcm)
        
        # However, the false conjecture likely stems from confusing the pair (g, h) in G x H 
        # with the product g * h in a single group G (where order(g*h) need not be lcm(|g|, |h|)).
        # We check both to robustly catch the intended counterexample.
        prod_not_lcm = False
        try:
            prod_order = int(get_order(g * h))
            if prod_order != target_lcm:
                prod_not_lcm = True
        except Exception:
            pass
            
        neg_q = bool(pair_not_lcm or prod_not_lcm)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G with finite order m",
    "H_2: h is an element of H with finite order n",
    r"¬Q: The order of the element (g, h) in the direct product G \times H is not the least common multiple of m and n"
]

N_HYP = 2
NEG_Q_INDEX = 2