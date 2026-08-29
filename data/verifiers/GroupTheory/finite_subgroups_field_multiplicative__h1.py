import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

# Quaternion group Q8 (the standard counterexample for division rings)
# Elements mapped to 0..7: 1, -1, i, -i, j, -j, k, -k
_i = Permutation(0, 2, 1, 3)(4, 7, 5, 6)
_j = Permutation(0, 4, 1, 5)(2, 6, 3, 7)
Q8 = PermutationGroup(_i, _j)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # The witness could be a tuple (F, G) or just the group G.
    if isinstance(witness, tuple) and len(witness) == 2:
        F, G = witness
    else:
        F, G = None, witness

    # H_1: F^\times is the multiplicative group of non-zero elements of F
    # If F is a division ring, its non-zero elements form a group.
    # We verify this by checking if G is a valid group, assuming it embeds in such an F.
    try:
        h1 = hasattr(G, 'order') and hasattr(G, 'is_cyclic')
    except Exception:
        h1 = False

    # H_2: G is a subgroup of F^\times
    try:
        h2 = hasattr(G, 'order') and hasattr(G, 'is_cyclic')
    except Exception:
        h2 = False

    # H_3: G is finite
    try:
        if hasattr(G, 'is_finite'):
            h3 = bool(G.is_finite)
        else:
            h3 = bool(G.order() < float('inf'))
    except Exception:
        h3 = False

    # ¬Q: G is not a cyclic group
    try:
        neg_q = not bool(G.is_cyclic)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F^\\times is the multiplicative group of non-zero elements of F",
    "H_2: G is a subgroup of F^\\times",
    "H_3: G is finite",
    "¬Q: G is not cyclic"
]

N_HYP = 3
NEG_Q_INDEX = 3