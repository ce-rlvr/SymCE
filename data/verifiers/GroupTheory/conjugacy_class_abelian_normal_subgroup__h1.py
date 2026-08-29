import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, A, a = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an abelian normal subgroup of G
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(A, PermutationGroup):
            if A.is_abelian:
                is_sub = True
                for gen in A.generators:
                    if gen not in G:
                        is_sub = False
                        break
                if is_sub:
                    h1 = True
                    for g in G.generators:
                        g_inv = ~g
                        for gen in A.generators:
                            if (g * gen * g_inv) not in A:
                                h1 = False
                                break
                        if not h1:
                            break
    except Exception:
        h1 = False

    # H_2: a is an element of A
    try:
        h2 = isinstance(a, Permutation) and (a in A)
    except Exception:
        h2 = False

    # ¬Q: The size of the conjugacy class of a in G does not divide the index of A in G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
            order_A = A.order() if callable(getattr(A, 'order', None)) else A.order
            index = order_G // order_A
            
            orbit = set()
            elements = list(G.generate()) if hasattr(G, 'generate') else list(G.elements)
            for g in elements:
                orbit.add(g * a * ~g)
            class_size = len(orbit)
            
            neg_q = (index % class_size) != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an abelian normal subgroup of G",
    "H_2: a is an element of A",
    "¬Q: The size of the conjugacy class of a in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2