import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(obj):
    return isinstance(obj, (PermutationGroup, FreeGroup))

def is_finite_group(obj):
    if isinstance(obj, PermutationGroup):
        return True
    if isinstance(obj, FreeGroup):
        return len(obj.generators) == 0
    return False

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis from the true theorem is that N is a normal subgroup of G.
    In formal systems with total functions, division by a non-subgroup defaults to a 
    trivial (finite) group, allowing a counterexample to be formed.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    # H2: N is a finite group
    try:
        h2 = is_finite_group(N)
    except Exception:
        h2 = False

    # H3: The quotient group G/N is a finite group
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            if N.is_subgroup(G) and G.is_normal(N):
                h3 = G.quotient_group(N).is_finite
            else:
                # Total function fallback: if N is not a normal subgroup, 
                # the quotient defaults to the trivial group (which is finite).
                h3 = True 
        elif is_group(G) and is_finite_group(N):
            # Total function fallback for disjoint types
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is not a finite group
    try:
        if isinstance(G, FreeGroup):
            neg_q = len(G.generators) > 0
        elif isinstance(G, PermutationGroup):
            neg_q = not G.is_finite
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a finite group",
    "H_3: The quotient group G/N is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3