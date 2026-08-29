import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The center of G is not a cyclic group of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (G, p)
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, p = witness
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # ¬Q: The center of G is not a cyclic group of order p
    try:
        # Get the center of the group
        try:
            C = G.center()
        except TypeError:
            C = G.center
            
        # Get the order of the center
        try:
            order_C = C.order()
        except TypeError:
            order_C = C.order
            
        if order_C == p:
            # If the order is p, check if it is cyclic by finding an element of order p
            try:
                elements = C.elements
            except TypeError:
                elements = C.elements()
            
            is_cyclic = False
            for g in elements:
                try:
                    o = g.order()
                except TypeError:
                    o = g.order
                if o == p:
                    is_cyclic = True
                    break
            neg_q = not is_cyclic
        else:
            # If the order is not p, it cannot be a cyclic group of order p
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]