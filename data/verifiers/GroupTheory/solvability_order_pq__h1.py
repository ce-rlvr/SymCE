import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    G, p, q = None, 0, 0
    
    # Unpack witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            if hasattr(witness[0], 'order'):
                G, p, q = witness
            elif hasattr(witness[2], 'order'):
                p, q, G = witness
            else:
                G, p, q = witness
        else:
            G = witness
            if hasattr(G, 'order'):
                order = G.order()
                factors = sympy.ntheory.factorint(order)
                if len(factors) == 2 and all(v == 1 for v in factors.values()):
                    p, q = list(factors.keys())
    except Exception:
        pass

    # H_1: p and q are distinct prime numbers
    try:
        h1 = bool(sympy.ntheory.isprime(p) and sympy.ntheory.isprime(q) and p != q)
    except Exception:
        h1 = False

    # H_2: The order of G is pq
    try:
        h2 = bool(G.order() == p * q)
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        solvable = G.is_solvable
        if callable(solvable):
            solvable = solvable()
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: The order of G is pq",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2