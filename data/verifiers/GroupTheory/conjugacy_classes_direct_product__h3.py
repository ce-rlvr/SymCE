import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, g, h = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g is an element of G
    try:
        h2 = g in G.elements
    except Exception:
        h2 = False

    # neg_Q: The conjugacy class of (g, h) in G x H is the Cartesian product of the conjugacy class of g in G and the conjugacy class of h in H.
    try:
        # If g is not in G or h is not in H, their conjugacy classes are undefined,
        # making the equality false (hence neg_Q is True).
        if g not in G.elements or h not in H.elements:
            neg_q = True
        else:
            cg = {x * g * ~x for x in G.elements}
            ch = {y * h * ~y for y in H.elements}
            cgh = {(x * g * ~x, y * h * ~y) for x in G.elements for y in H.elements}
            cartesian = {(a, b) for a in cg for b in ch}
            neg_q = not (cgh == cartesian)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: g is an element of G",
    "¬Q: The conjugacy class of (g, h) in G x H is not the Cartesian product of the conjugacy class of g in G and the conjugacy class of h in H"
]

N_HYP = 2
NEG_Q_INDEX = 2