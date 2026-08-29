import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    "¬Q: The cardinality of the conjugacy class of x does NOT divide the order of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # The witness can be a tuple (G, x) or just a group G.
    if isinstance(witness, tuple) and len(witness) == 2:
        G, x = witness
        elements_to_check = [x]
    else:
        G = witness
        try:
            elements_to_check = list(G.elements)
        except Exception:
            elements_to_check = []

    # H_1: G is a finite group
    try:
        order_G = G.order()
        h1_ok = order_G > 0 and order_G < float('inf')
    except Exception:
        h1_ok = False

    # ¬Q: The cardinality of the conjugacy class of x does NOT divide the order of G
    neg_q_ok = False
    try:
        if h1_ok:
            for elem in elements_to_check:
                class_size = None
                
                # Fast path for PermutationGroup using the centralizer
                if isinstance(G, PermutationGroup):
                    try:
                        C = G.centralizer(PermutationGroup([elem]))
                        class_size = order_G // C.order()
                    except Exception:
                        pass
                
                # Fallback path: compute the orbit under conjugation
                if class_size is None:
                    orbit = set()
                    if hasattr(G, 'generate_dimino'):
                        gen = G.generate_dimino()
                    elif hasattr(G, 'elements'):
                        gen = G.elements
                    else:
                        gen = []
                        
                    for g in gen:
                        try:
                            conj = g * elem * ~g
                        except Exception:
                            conj = g * elem * g**-1
                        orbit.add(conj)
                    class_size = len(orbit)
                
                if class_size > 0 and order_G % class_size != 0:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]