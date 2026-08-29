import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # The witness could be a group G, or a sequence representing a subnormal series where G is the first element.
    if isinstance(witness, (list, tuple)) and len(witness) > 0:
        G = witness[0]
    else:
        G = witness

    # H_1: G possesses a subnormal series in which every factor group is cyclic
    h1 = False
    try:
        if hasattr(G, 'is_polycyclic'):
            val = G.is_polycyclic
            h1 = bool(val() if callable(val) else val)
        elif hasattr(G, 'has_cyclic_subnormal_series'):
            val = G.has_cyclic_subnormal_series
            h1 = bool(val() if callable(val) else val)
        elif hasattr(G, 'is_solvable'):
            # For finite groups (like sympy's PermutationGroup), being polycyclic is equivalent to being solvable.
            val = G.is_solvable
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # Q: G is a solvable group
    q = True
    try:
        if hasattr(G, 'is_solvable'):
            val = G.is_solvable
            q = bool(val() if callable(val) else val)
    except Exception:
        q = True

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: G possesses a subnormal series in which every factor group is cyclic",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1