import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    R, G = None, None
    if isinstance(witness, tuple):
        if len(witness) >= 2:
            R, G = witness[0], witness[1]
        elif len(witness) == 1:
            G = witness[0]
    else:
        G = witness

    # H_1: R is a commutative ring
    h1 = True
    if R is not None:
        try:
            if hasattr(R, 'is_commutative') and R.is_commutative is not None:
                h1 = bool(R.is_commutative)
        except Exception:
            h1 = False

    # H_2: R G is the group ring of G over R
    h2 = True
    
    # H_3: Delta is the augmentation ideal of R G
    h3 = True
    
    # ¬Q: The quotient ring R G / Delta is not isomorphic to R
    # The conclusion R G / Delta isomorphic to R holds for any non-empty group or monoid.
    # It fails if G is empty (since R[empty] = 0, and 0 is not isomorphic to R for R != 0).
    # We check if G is empty or not a valid group.
    try:
        is_valid_group = False
        if G is not None:
            if hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
                is_valid_group = order >= 1
            elif hasattr(G, 'elements'):
                is_valid_group = len(list(G.elements)) >= 1
            elif hasattr(G, '__len__'):
                is_valid_group = len(G) >= 1
    except Exception:
        is_valid_group = False

    neg_q = not is_valid_group
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R G is the group ring of G over R",
    "H_3: Delta is the augmentation ideal of R G",
    "¬Q: The quotient ring R G / Delta is not isomorphic to R"
]

N_HYP = 3
NEG_Q_INDEX = 3