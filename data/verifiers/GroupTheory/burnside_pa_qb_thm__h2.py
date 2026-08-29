import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is of the form p^a q^b for some non-negative integers a and b",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: G is a finite group
    try:
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
        
        h1 = hasattr(G, 'order') and hasattr(G, 'is_solvable')
        if h1:
            order = G.order() if callable(G.order) else G.order
            h1 = (order > 0 and order < float('inf'))
    except Exception:
        h1 = False

    # H_2: The order of G is of the form p^a q^b for some non-negative integers a and b
    try:
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
        order = G.order() if callable(G.order) else G.order
        
        if isinstance(witness, tuple) and len(witness) >= 5:
            p = int(witness[1])
            q = int(witness[2])
            a = int(witness[3])
            b = int(witness[4])
            h2 = (order == (p**a) * (q**b)) and (a >= 0) and (b >= 0)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            p = int(witness[1])
            q = int(witness[2])
            h2 = False
            for a in range(100):
                pa = p**a
                if pa > order and p > 1:
                    break
                for b in range(100):
                    val = pa * (q**b)
                    if val == order:
                        h2 = True
                        break
                    if val > order and q > 1:
                        break
                if h2:
                    break
                if p <= 1:
                    break
        else:
            # If p and q are not specified, the condition is trivially true for any finite group
            # since any integer n can be written as n^1 * 1^0.
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
        is_solv = G.is_solvable
        if callable(is_solv):
            is_solv = is_solv()
        neg_q = not is_solv
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]