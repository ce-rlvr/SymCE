import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Z(G) is the center of G",
    "¬Q: The size of the conjugacy class of x does not divide the index of Z(G) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            Z = witness.get('Z', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                Z = None
            elif len(witness) == 3:
                G, Z, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = getattr(G, 'is_finite', False)
            if not h1:
                order = G.order()
                h1 = (order < float('inf'))
    except Exception:
        h1 = False

    try:
        center = G.center()
        if Z is None:
            Z = center
            h2 = True
        else:
            h2 = (Z.is_subgroup(center) and center.is_subgroup(Z)) or (Z == center)
    except Exception:
        h2 = False

    try:
        order_G = G.order()
        order_Z = Z.order()
        index = order_G // order_Z
        
        orbit = set()
        for g in G.elements:
            orbit.add(g * x * (~g))
        class_size = len(orbit)
        
        neg_q = (index % class_size != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]