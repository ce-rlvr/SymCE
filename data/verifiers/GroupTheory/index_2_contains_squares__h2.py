import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, g)
    """
    try:
        G, H, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The index of H in G is equal to 2
    try:
        if hasattr(H, 'order'):
            h_order = H.order() if callable(H.order) else H.order
        else:
            h_order = len(H)
            
        if hasattr(G, 'order'):
            g_order = G.order() if callable(G.order) else G.order
        else:
            g_order = len(G)
            
        h2 = (g_order == 2 * h_order)
    except Exception:
        h2 = False

    # H_3: g is an element of G
    try:
        if hasattr(G, 'contains') and callable(G.contains):
            h3 = G.contains(g)
        elif hasattr(G, 'elements'):
            h3 = g in G.elements
        else:
            h3 = g in G
    except Exception:
        h3 = False

    # ¬Q: g^2 is not in H
    try:
        g2 = g**2
        if hasattr(H, 'contains') and callable(H.contains):
            neg_q = not H.contains(g2)
        elif hasattr(H, 'elements'):
            neg_q = g2 not in H.elements
        else:
            neg_q = g2 not in H
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is equal to 2",
    "H_3: g is an element of G",
    "¬Q: g^2 is not in H"
]

N_HYP = 3
NEG_Q_INDEX = 3