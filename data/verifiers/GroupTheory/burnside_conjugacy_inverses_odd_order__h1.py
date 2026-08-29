import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
        G, x = witness
    except Exception:
        return [False, False, False]
    
    # H1: The order of G is an odd integer
    try:
        if hasattr(G, 'order'):
            order = G.order()
        else:
            order = len(G)
        h1 = (int(order) % 2 == 1)
    except Exception:
        h1 = False

    # H2: x is a non-identity element of G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        in_G = any(e == x for e in elements)
        # In a multiplicative structure, only the identity satisfies x * x == x
        is_id = (x * x == x)
        h2 = in_G and not is_id
    except Exception:
        h2 = False

    # ¬Q: x is conjugate to x^-1 in G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        x_inv = x**-1
        neg_q = False
        for g in elements:
            try:
                if g * x * g**-1 == x_inv:
                    neg_q = True
                    break
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an odd integer",
    "H_2: x is a non-identity element of G",
    "¬Q: x is conjugate to x^-1 in G"
]

N_HYP = 2
NEG_Q_INDEX = 2