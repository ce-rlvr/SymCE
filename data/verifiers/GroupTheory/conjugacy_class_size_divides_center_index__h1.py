import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x does not divide the index of Z(G) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                Z_provided = None
            elif len(witness) == 3:
                G, Z_provided, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: Z(G) is the center of G
    try:
        if hasattr(G, 'center'):
            Z_actual = G.center() if callable(G.center) else G.center
        elif hasattr(G, 'Z'):
            Z_actual = G.Z() if callable(G.Z) else G.Z
        else:
            Z_actual = None
            
        if Z_provided is not None:
            if Z_actual is not None:
                h1 = (Z_provided == Z_actual)
            else:
                h1 = True
            Z = Z_provided
        else:
            if Z_actual is not None:
                h1 = True
                Z = Z_actual
            else:
                h1 = False
                Z = None
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(x) if callable(G.contains) else G.contains)
        elif hasattr(G, '__contains__'):
            h2 = bool(x in G)
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The size of the conjugacy class of x does NOT divide the index of Z(G) in G
    try:
        class_size = None
        if hasattr(G, 'conjugacy_class_size'):
            class_size = G.conjugacy_class_size(x) if callable(G.conjugacy_class_size) else G.conjugacy_class_size
        elif hasattr(G, 'centralizer'):
            if isinstance(G, PermutationGroup):
                C = G.centralizer(PermutationGroup([x]))
            else:
                C = G.centralizer(x) if callable(G.centralizer) else G.centralizer
            g_order = G.order() if callable(G.order) else G.order
            c_order = C.order() if callable(C.order) else C.order
            class_size = g_order // c_order
            
        index_Z = None
        if hasattr(G, 'index'):
            index_Z = G.index(Z) if callable(G.index) else G.index
        elif hasattr(G, 'order') and hasattr(Z, 'order'):
            g_order = G.order() if callable(G.order) else G.order
            z_order = Z.order() if callable(Z.order) else Z.order
            index_Z = g_order // z_order
            
        if class_size is None or index_Z is None:
            neg_q = False
        else:
            if index_Z == sympy.oo or index_Z == math.inf:
                neg_q = True
            elif class_size == sympy.oo or class_size == math.inf:
                neg_q = True
            elif class_size == 0:
                neg_q = True
            else:
                neg_q = (int(index_Z) % int(class_size) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]