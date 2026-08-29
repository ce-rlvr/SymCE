import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, x, y = witness
            n = None
        elif len(witness) == 4:
            G, x, y, n = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        is_g = False
        if isinstance(G, PermutationGroup):
            is_g = True
        elif hasattr(G, 'generators') and hasattr(G, 'identity'):
            is_g = True
        h1_ok = is_g
    except Exception:
        h1_ok = False

    # H_2: x is an element of G
    try:
        h2_ok = (x in G)
    except Exception:
        try:
            h2_ok = G.contains(x)
        except Exception:
            h2_ok = False

    # H_3: y is an element of G
    try:
        h3_ok = (y in G)
    except Exception:
        try:
            h3_ok = G.contains(y)
        except Exception:
            h3_ok = False

    # ¬Q: The product yx does not have finite order n
    try:
        yx = y * x
        order_val = None
        
        if isinstance(yx, Permutation):
            order_val = yx.order()
        else:
            try:
                order_val = yx.order()
            except Exception:
                order_val = float('inf')
        
        if n is not None:
            neg_q_ok = (order_val != n)
        else:
            neg_q_ok = (order_val == float('inf'))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "¬Q: The product yx does not have finite order n"
]

N_HYP = 3
NEG_Q_INDEX = 3