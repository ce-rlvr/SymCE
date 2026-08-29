import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide both a group G and an integer n.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'center'):
                G, n = witness
            else:
                n, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Check H_1: n >= 1
    try:
        h1 = (int(n) == n) and (n >= 1)
    except Exception:
        h1 = False

    # Check ¬Q: The center of G is NOT isomorphic to Z/nZ
    try:
        C = G.center()
        order_C = C.order()
        
        if order_C != n:
            is_iso = False
        else:
            if n == 1:
                is_iso = True
            else:
                # For finite abelian groups, it is cyclic iff it has an element of order n
                is_iso = any(g.order() == n for g in C.elements)
                
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "¬Q: The center of G is not isomorphic to Z/nZ"
]

N_HYP = 1
NEG_Q_INDEX = 1