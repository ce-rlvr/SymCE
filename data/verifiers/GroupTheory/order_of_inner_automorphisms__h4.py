import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
        G, g = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'identity'):
            identity = G.identity
        elif hasattr(g, '__invert__'):
            identity = g * ~g
        elif hasattr(g, 'inv'):
            identity = g * g.inv()
        else:
            identity = g**0
        h1 = hasattr(G, 'generators')
    except Exception:
        h1 = False

    # H2: g is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(g))
        else:
            h2 = bool(g in G)
    except Exception:
        h2 = False

    # H3: There exists a positive integer n such that g^n = e, and n is the smallest such integer
    try:
        if hasattr(g, 'order') and callable(g.order):
            n = g.order()
        else:
            n = None
            curr = g
            for i in range(1, 2000):
                if curr == identity:
                    n = i
                    break
                curr = curr * g
        h3 = (n is not None and n > 0)
    except Exception:
        h3 = False

    # neg_Q: The order of \phi_g in Aut(G) does NOT divide n
    try:
        if not h3:
            neg_q = False
        else:
            m = None
            gm = g
            for i in range(1, n + 1):
                commutes = True
                for x in G.generators:
                    if gm * x != x * gm:
                        commutes = False
                        break
                if commutes:
                    m = i
                    break
                gm = gm * g
            
            if m is None:
                neg_q = False
            else:
                neg_q = (n % m != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: There exists a positive integer n such that g^n = e, and n is the smallest such integer",
    "¬Q: The order of phi_g in Aut(G) does not divide n"
]

N_HYP = 3
NEG_Q_INDEX = 3