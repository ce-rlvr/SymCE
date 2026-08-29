import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    AbelianGroup
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
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (G, H, phi) where:
      - G is the domain group
      - H is the codomain group
      - phi is a map (dictionary or callable) from G to H
    """
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a torsion group (every element has finite order)
    try:
        h1 = False
        if hasattr(G, 'elements'):
            h1 = True
            for g in G.elements:
                if not hasattr(g, 'order'):
                    h1 = False
                    break
                ord_g = g.order()
                if ord_g == float('inf') or ord_g == 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: H is a torsion-free group (only the identity has finite order)
    try:
        h2 = False
        identity = None
        if H == sympy.S.Integers or H == Z:
            h2 = True
            identity = 0
        elif type(H).__name__ == 'FreeGroup':
            h2 = True
            identity = H.identity
        elif hasattr(H, 'elements'):
            h2 = True
            identity = H.identity
            for h in H.elements:
                if not hasattr(h, 'order'):
                    h2 = False
                    break
                if h != identity:
                    ord_h = h.order()
                    if ord_h < float('inf') and ord_h > 0:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: phi is NOT the trivial homomorphism
    # (i.e., it is a valid map from G to H, but does not map all elements to the identity)
    try:
        is_trivial = True
        for g in G.elements:
            val = phi[g] if isinstance(phi, dict) else phi(g)
            if val != identity:
                is_trivial = False
                break
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a torsion group",
    "H_2: H is a torsion-free group",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2