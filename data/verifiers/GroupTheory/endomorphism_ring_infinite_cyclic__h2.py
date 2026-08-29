import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_infinite_cyclic(G):
    """Check if the given object represents an infinite cyclic group."""
    if G is sympy.S.Integers or G is sympy.ZZ:
        return True
    try:
        if type(G).__name__ == 'FreeGroup':
            return len(G.generators) == 1
    except Exception:
        pass
    try:
        if type(G).__name__ == 'FpGroup':
            return list(G.abelian_invariants()) == [0]
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: G is an infinite cyclic group
    try:
        h1_ok = is_infinite_cyclic(witness)
    except Exception:
        h1_ok = False

    # ¬Q: End(G) is NOT isomorphic to the ring of integers Z.
    # For finitely generated groups (which covers all SymPy group representations),
    # End(G) is isomorphic to Z if and only if G is infinite cyclic.
    try:
        q_ok = is_infinite_cyclic(witness)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is an infinite cyclic group",
    "¬Q: End(G) is not isomorphic to the ring of integers Z"
]

N_HYP = 1
NEG_Q_INDEX = 1