import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
        G, x, z = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
    except Exception:
        return [False, False, False]
        
    # H_1: Let x be an element of G.
    try:
        h1 = x in elements
    except Exception:
        h1 = False
        
    # H_2: Let z be an element in the center Z(G).
    try:
        h2 = (z in elements) and all(z * g == g * z for g in elements)
    except Exception:
        h2 = False
        
    # ¬Q: The conjugacy class of zx is NOT equal to the set {z * y | y is conjugate to x in G}.
    # In the general context (including semigroups, which provide the counterexample when the group hypothesis is dropped),
    # y is conjugate to x if there exist u, v in G such that x = u*v and y = v*u.
    try:
        # Compute the conjugacy class of x
        Cx = []
        for u in elements:
            for v in elements:
                if u * v == x:
                    vu = v * u
                    if vu not in Cx:
                        Cx.append(vu)
                        
        # Compute the conjugacy class of zx
        zx = z * x
        Czx = []
        for u in elements:
            for v in elements:
                if u * v == zx:
                    vu = v * u
                    if vu not in Czx:
                        Czx.append(vu)
                        
        # Compute the set {z * y | y in Cx}
        zCx = []
        for y in Cx:
            zy = z * y
            if zy not in zCx:
                zCx.append(zy)
                
        # Check if Czx == zCx
        is_subset1 = all(item in zCx for item in Czx)
        is_subset2 = all(item in Czx for item in zCx)
        neg_q = not (is_subset1 and is_subset2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: z is an element in the center Z(G)",
    "¬Q: The conjugacy class of zx is not equal to {z * y | y is conjugate to x in G}"
]

N_HYP = 2
NEG_Q_INDEX = 2