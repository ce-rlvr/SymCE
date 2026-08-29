import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness can be a tuple (G, n) or just G (in which case n is inferred as G.order() / 2).
    """
    # Extract G and n
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            if hasattr(G, 'order'):
                order_attr = G.order
                if callable(order_attr):
                    order = order_attr()
                else:
                    order = order_attr
                n = order / 2
            else:
                n = None
    except Exception:
        G = witness
        n = None

    # H_1: n is an odd integer
    try:
        h1 = False
        if n is not None:
            if isinstance(n, (int, sympy.Integer)):
                h1 = (n % 2 == 1)
            elif isinstance(n, float) and n.is_integer():
                h1 = (int(n) % 2 == 1)
            elif hasattr(n, 'is_integer') and n.is_integer:
                h1 = (int(n) % 2 == 1)
    except Exception:
        h1 = False

    # H_2: The order of G is exactly 2n
    try:
        h2 = False
        if hasattr(G, 'order'):
            order_attr = G.order
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
            h2 = (order == 2 * n)
    except Exception:
        h2 = False

    # ¬Q: G does NOT contain a normal subgroup of order n
    try:
        has_normal = False
        if hasattr(G, 'normal_subgroups'):
            ns_attr = G.normal_subgroups
            if callable(ns_attr):
                ns = ns_attr()
            else:
                ns = ns_attr
            
            for H in ns:
                if hasattr(H, 'order'):
                    H_order_attr = H.order
                    if callable(H_order_attr):
                        H_order = H_order_attr()
                    else:
                        H_order = H_order_attr
                    
                    if H_order == n:
                        has_normal = True
                        break
        
        neg_q = not has_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd integer",
    "H_2: The order of G is exactly 2n",
    "¬Q: G does not contain a normal subgroup of order n"
]

N_HYP = 2
NEG_Q_INDEX = 2