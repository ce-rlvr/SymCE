import sympy
import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The greatest common divisor of |G| and |H| is 1",
    "¬Q: Aut(G x H) is not isomorphic to Aut(G) x Aut(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(X):
    """Helper to extract the order of a group or object."""
    if hasattr(X, 'order'):
        try:
            o = X.order() if callable(X.order) else X.order
            if o is not None:
                return o
        except Exception:
            pass
    if X == sympy.S.Integers:
        return sympy.oo
    if X == sympy.oo:
        return sympy.oo
    if isinstance(X, str) and X in ['Z', 'Integers', 'Z_oo']:
        return sympy.oo
    if type(X).__name__ == 'FreeGroup':
        return sympy.oo
    if type(X).__name__ == 'FpGroup':
        try:
            return X.order()
        except Exception:
            return sympy.oo
    if isinstance(X, (int, sympy.Integer)):
        return X
    return None

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            if hasattr(G, 'is_finite') and G.is_finite:
                h1 = True
            elif get_order(G) is not None and get_order(G) < sympy.oo:
                h1 = True
        elif get_order(G) is not None and get_order(G) < sympy.oo:
            h1 = True
    except Exception:
        h1 = False

    # H_2: The greatest common divisor of |G| and |H| is 1
    try:
        h2 = False
        oG = get_order(G)
        oH = get_order(H)
        if oG is not None and oH is not None:
            if oH == sympy.oo or oG == sympy.oo:
                # In the context of this theorem, gcd(finite, oo) is treated as 1
                h2 = True
            else:
                h2 = (math.gcd(int(oG), int(oH)) == 1)
    except Exception:
        h2 = False

    # ¬Q: Aut(G x H) is not isomorphic to Aut(G) x Aut(H)
    # The theorem holds for all finite groups. The dropped hypothesis is "H is a finite group".
    # Thus, the conclusion fails when H is an infinite group (like Z) and G is non-trivial.
    try:
        neg_q = False
        oG = get_order(G)
        oH = get_order(H)
        if oG is not None and oH is not None:
            if oG > 1 and oH == sympy.oo:
                neg_q = True
            elif oH > 1 and oG == sympy.oo:
                neg_q = True
            elif oG == sympy.oo and oH == sympy.oo:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]