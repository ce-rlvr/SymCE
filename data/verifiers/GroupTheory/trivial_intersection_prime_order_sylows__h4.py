import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, p, P, Q = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: p divides the order of G
    try:
        order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
        h3 = bool(order_G % p == 0)
    except Exception:
        h3 = False

    # H_4: P and Q are distinct Sylow p-subgroups of G
    try:
        if not (isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup)):
            h4 = False
        else:
            order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
            k = 0
            while order_G % (p**(k+1)) == 0:
                k += 1
            sylow_order = p**k
            
            P_is_subgroup = all(g in G for g in P.generators)
            Q_is_subgroup = all(g in G for g in Q.generators)
            
            order_P = P.order() if callable(getattr(P, 'order', None)) else P.order
            order_Q = Q.order() if callable(getattr(Q, 'order', None)) else Q.order
            
            P_order_ok = (order_P == sylow_order)
            Q_order_ok = (order_Q == sylow_order)
            
            P_elems = set(P.generate())
            Q_elems = set(Q.generate())
            distinct = (P_elems != Q_elems)
            
            h4 = bool(P_is_subgroup and Q_is_subgroup and P_order_ok and Q_order_ok and distinct)
    except Exception:
        h4 = False

    # ¬Q: The intersection P \cap Q is not the trivial subgroup {e}
    try:
        P_elems = set(P.generate())
        Q_elems = set(Q.generate())
        intersection = P_elems.intersection(Q_elems)
        neg_q = len(intersection) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: p divides the order of G",
    "H_4: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {e}"
]

N_HYP = 4
NEG_Q_INDEX = 4