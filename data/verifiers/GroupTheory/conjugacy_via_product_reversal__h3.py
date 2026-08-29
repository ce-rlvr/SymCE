import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, a, b).
    """
    try:
        G, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements')
        if h1:
            elements = list(G.elements)
    except Exception:
        h1 = False

    # H_2: a is an element of G
    try:
        h2 = a in elements
    except Exception:
        h2 = False

    # ¬Q: (a and b are conjugate in G) is not equivalent to (there exist x, y in G such that a = xy and b = yx)
    try:
        # P: a and b are conjugate in G
        P = False
        for g in elements:
            try:
                ginv = g**-1
            except Exception:
                try:
                    ginv = ~g
                except Exception:
                    continue
            try:
                if b == ginv * a * g or b == g * a * ginv:
                    P = True
                    break
            except Exception:
                pass

        # Q: there exist x, y in G such that a = xy and b = yx
        Q = False
        for x in elements:
            for y in elements:
                try:
                    if a == x * y and b == y * x:
                        Q = True
                        break
                except Exception:
                    pass
            if Q:
                break

        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: a is an element of G",
    "¬Q: (a and b are conjugate in G) is not equivalent to (there exist x, y in G such that a = xy and b = yx)"
]

N_HYP = 2
NEG_Q_INDEX = 2