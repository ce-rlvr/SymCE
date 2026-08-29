import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        if h1 and isinstance(x, Permutation):
            try:
                h2 = x in G
            except Exception:
                h2 = x in list(G.generate())
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: y is an element of G
    try:
        if h1 and isinstance(y, Permutation):
            try:
                h3 = y in G
            except Exception:
                h3 = y in list(G.generate())
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: C_G(x) is NOT isomorphic to C_G(y)
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            elements = list(G.generate())
            C_x_elems = [g for g in elements if g * x == x * g]
            C_y_elems = [g for g in elements if g * y == y * g]
            
            C_x = PermutationGroup(*C_x_elems)
            C_y = PermutationGroup(*C_y_elems)
            
            is_iso = None
            if hasattr(C_x, 'is_isomorphic'):
                try:
                    is_iso = C_x.is_isomorphic(C_y)
                except Exception:
                    pass
            
            if is_iso is None:
                if C_x.order() != C_y.order():
                    is_iso = False
                elif C_x.is_abelian != C_y.is_abelian:
                    is_iso = False
                else:
                    orders_x = sorted([g.order() for g in C_x.generate()])
                    orders_y = sorted([g.order() for g in C_y.generate()])
                    if orders_x != orders_y:
                        is_iso = False
                    else:
                        is_iso = True
                        
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "¬Q: C_G(x) is not isomorphic to C_G(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3