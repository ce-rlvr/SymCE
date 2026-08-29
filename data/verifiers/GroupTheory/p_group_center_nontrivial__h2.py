import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        p, G = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    try:
        order_attr = getattr(G, 'order')
        order = order_attr() if callable(order_attr) else order_attr
        if order == 1:
            h2 = True
        else:
            factors = factorint(order)
            h2 = [int(k) for k in factors.keys()] == [int(p)]
    except Exception:
        h2 = False
        
    try:
        C = G.center()
        if hasattr(C, 'order'):
            c_order_attr = getattr(C, 'order')
            c_order = c_order_attr() if callable(c_order_attr) else c_order_attr
        else:
            c_order = len(C)
        neg_q = bool(c_order <= 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite group of order p^n",
    "¬Q: The center of G, Z(G), has order <= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2