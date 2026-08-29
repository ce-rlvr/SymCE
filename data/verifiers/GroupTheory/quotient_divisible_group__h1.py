import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a divisible group
    try:
        if hasattr(G, 'is_divisible'):
            h1 = G.is_divisible() if callable(G.is_divisible) else G.is_divisible
        else:
            # For finite groups (like SymPy's PermutationGroup), 
            # the only divisible group is the trivial group.
            h1 = (G.order() == 1)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = H.is_subgroup(G)
        elif hasattr(G, 'is_subgroup'):
            h2 = G.is_subgroup(H)
        else:
            h2 = H.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: The quotient group G/H is NOT a divisible abelian group
    try:
        is_normal = False
        if hasattr(H, 'is_normal'):
            is_normal = H.is_normal(G)
        elif hasattr(G, 'is_normal'):
            is_normal = G.is_normal(H)
        else:
            is_normal = H.is_normal(G)

        if not is_normal:
            # If H is not a normal subgroup, G/H is not a group, 
            # hence it is not a divisible abelian group.
            neg_q = True
        else:
            # Check if G/H is abelian
            is_ab = False
            if hasattr(G, 'quotient_group'):
                Q_grp = G.quotient_group(H)
                if hasattr(Q_grp, 'is_abelian'):
                    is_ab = Q_grp.is_abelian() if callable(Q_grp.is_abelian) else Q_grp.is_abelian
                else:
                    is_ab = False
            else:
                # Fallback for SymPy groups: G/H is abelian iff the derived subgroup of G is contained in H
                is_ab = G.derived_subgroup().is_subgroup(H)

            # Check if G/H is divisible
            is_div = False
            if hasattr(G, 'quotient_group'):
                Q_grp = G.quotient_group(H)
                if hasattr(Q_grp, 'is_divisible'):
                    is_div = Q_grp.is_divisible() if callable(Q_grp.is_divisible) else Q_grp.is_divisible
                else:
                    is_div = (Q_grp.order() == 1)
            else:
                # Fallback for finite groups: quotient is divisible iff it is trivial
                is_div = (G.order() == H.order())

            neg_q = not (is_ab and is_div)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a divisible group",
    "H_2: H is a subgroup of G",
    "¬Q: The quotient group G/H is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2