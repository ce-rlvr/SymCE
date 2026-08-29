import sympy
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
    # The witness can be either a tuple (G, x) or just a group G.
    # If it's just G, we default x to the identity element, which is the standard 
    # counterexample for the dropped hypothesis (x != e).
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G = witness
            x = None
    except Exception:
        G = witness
        x = None

    def get_elements(group):
        try:
            els = group.elements
            if callable(els):
                return list(els())
            return list(els)
        except Exception:
            return []

    elements = get_elements(G)
    
    if x is None and elements:
        try:
            # Default to the identity element
            x = elements[0] * elements[0]**-1
        except Exception:
            pass

    # H_1: G is a finite group
    h1_ok = False
    try:
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            if isinstance(order, (int, sympy.Integer)) and order > 0:
                if elements:
                    h1_ok = True
    except Exception:
        pass

    # H_2: The order of G is an odd integer
    h2_ok = False
    try:
        if h1_ok:
            order = G.order() if callable(G.order) else G.order
            if order % 2 == 1:
                h2_ok = True
    except Exception:
        pass

    # ¬Q: x is conjugate to x^(-1) in G
    neg_q_ok = False
    try:
        if h1_ok and x is not None:
            if x in elements:
                try:
                    x_inv = x**-1
                except Exception:
                    x_inv = ~x
                
                for g in elements:
                    if g * x * g**-1 == x_inv:
                        neg_q_ok = True
                        break
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is an odd integer",
    "¬Q: x is conjugate to x^(-1) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2