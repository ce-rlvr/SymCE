import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    # Unpack witness. It could be a tuple (G, C_list) or just G.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, C_list = witness
        else:
            G = witness
            C_list = []
    except Exception:
        G = witness
        C_list = []

    # H_1: G is a finite group
    try:
        h1 = False
        if isinstance(G, PermutationGroup) or (hasattr(G, 'order') and hasattr(G, 'center')):
            order_G = G.order() if callable(G.order) else G.order
            if isinstance(order_G, (int, sympy.Integer)):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The order of G is NOT equal to the order of Z(G) plus the sum of the sizes of C_1, C_2, ..., C_k
    try:
        Z = G.center()
        order_Z = Z.order() if callable(Z.order) else Z.order
        order_G = G.order() if callable(G.order) else G.order
        
        if C_list is None:
            sum_C = 0
        elif isinstance(C_list, (int, float, sympy.Integer, sympy.Rational)):
            sum_C = int(C_list)
        else:
            sum_C = 0
            for C in C_list:
                if isinstance(C, (int, float, sympy.Integer, sympy.Rational)):
                    sum_C += int(C)
                elif hasattr(C, '__len__'):
                    sum_C += len(C)
                else:
                    sum_C += 1
                    
        q = (order_G == order_Z + sum_C)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The order of G is not equal to the order of Z(G) plus the sum of the sizes of C_1, C_2, ..., C_k"
]

N_HYP = 1
NEG_Q_INDEX = 1