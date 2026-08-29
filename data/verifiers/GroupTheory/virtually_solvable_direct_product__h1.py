import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def is_virtually_solvable(G):
    if hasattr(G, 'is_virtually_solvable'):
        val = G.is_virtually_solvable
        return val() if callable(val) else val
    if hasattr(G, 'is_solvable'):
        val = G.is_solvable
        return val() if callable(val) else val
    return False

def get_direct_product(G, H):
    try:
        from sympy.combinatorics import DirectProduct
        return DirectProduct(G, H)
    except Exception:
        pass
    try:
        return G * H
    except Exception:
        pass
    
    # Fallback mock object that correctly simulates the solvability of a direct product
    class MockProduct:
        def __init__(self, g, h):
            self.g = g
            self.h = h
        @property
        def is_virtually_solvable(self):
            return is_virtually_solvable(self.g) and is_virtually_solvable(self.h)
        @property
        def is_solvable(self):
            return is_virtually_solvable(self.g) and is_virtually_solvable(self.h)
            
    return MockProduct(G, H)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(is_virtually_solvable(H))
    except Exception:
        h1_ok = False

    try:
        GxH = get_direct_product(G, H)
        neg_q = not bool(is_virtually_solvable(GxH))
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a virtually solvable group",
    "¬Q: The direct product G × H is not a virtually solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1