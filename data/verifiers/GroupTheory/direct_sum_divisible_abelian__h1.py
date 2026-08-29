import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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

def is_abelian_group(G):
    if hasattr(G, 'is_abelian'):
        if callable(G.is_abelian):
            return bool(G.is_abelian())
        return bool(G.is_abelian)
    return False

def is_divisible(G):
    if hasattr(G, 'is_divisible'):
        if callable(G.is_divisible):
            return bool(G.is_divisible())
        return bool(G.is_divisible)
    if hasattr(G, 'order'):
        try:
            # For finite groups, the only divisible group is the trivial group.
            return G.order() == 1
        except Exception:
            pass
    return False

def conditions(witness) -> list[bool]:
    # Check if the witness is a custom object representing a family of groups
    try:
        if hasattr(witness, 'is_abelian_family'):
            h1 = bool(witness.is_abelian_family)
            h2 = bool(witness.is_divisible_family)
            neg_q = not bool(witness.is_direct_sum_divisible)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Otherwise, assume the witness is an iterable of group objects
    try:
        groups = list(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = all(is_abelian_group(G) for G in groups)
    except Exception:
        h1 = False

    try:
        h2 = all(is_divisible(G) for G in groups)
    except Exception:
        h2 = False

    try:
        # The direct sum of a finite family of groups is divisible 
        # if and only if each component group is divisible.
        is_ds_divisible = all(is_divisible(G) for G in groups)
        neg_q = not is_ds_divisible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {D_i} is a family of abelian groups indexed by I",
    "H_2: For every i in I, D_i is a divisible abelian group",
    "¬Q: The direct sum ⊕_{i ∈ I} D_i is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2