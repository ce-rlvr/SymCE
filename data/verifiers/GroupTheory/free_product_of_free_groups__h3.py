import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup

# Top-level setup: named object bindings for witness expressions
F1, x = free_group("x")
Z2 = FpGroup(F1, [x**2])
Z3 = FpGroup(F1, [x**3])

F2, a, b = free_group("a, b")
Z2_Z2 = FpGroup(F2, [a**2, b**2])
Z2_Z3 = FpGroup(F2, [a**2, b**3])

F3, c, d, e = free_group("c, d, e")
Z2_Z2_Z2 = FpGroup(F3, [c**2, d**2, e**2])

def conditions(witness) -> list[bool]:
    # Unpack witness. Accept either (I, F_family, F) or (F_family, F)
    try:
        if len(witness) == 3:
            I, F_family, F = witness
        elif len(witness) == 2:
            F_family, F = witness
            if isinstance(F_family, dict):
                I = list(F_family.keys())
            else:
                I = list(range(len(F_family)))
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: I is an index set
    try:
        h1 = isinstance(I, (list, tuple, set))
    except Exception:
        h1 = False

    # H_2: {F_i} is a family of groups
    try:
        if isinstance(F_family, dict):
            groups = list(F_family.values())
        else:
            groups = list(F_family)
        h2 = all(isinstance(G, FpGroup) for G in groups)
    except Exception:
        h2 = False

    # H_3: F is the free product of the groups {F_i}
    try:
        if not isinstance(F, FpGroup):
            h3 = False
        else:
            # A simple structural check for the free product:
            # The number of generators and relators should be the sum of those of the factors.
            gen_count = sum(len(G.generators) for G in groups)
            rel_count = sum(len(G.relators) for G in groups)
            h3 = (len(F.generators) == gen_count) and (len(F.relators) == rel_count)
    except Exception:
        h3 = False

    # ¬Q: F is not a free group
    try:
        # A free group must have a torsion-free abelianization.
        # abelian_invariants() returns the invariant factors of the abelianization.
        # 0 means Z (free part), 1 means trivial, >1 means Z_k (torsion).
        # If there is any invariant > 1, the group has torsion in its abelianization,
        # which means it cannot be a free group.
        invs = F.abelian_invariants()
        neg_q = any(abs(inv) > 1 for inv in invs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: {F_i} is a family of groups",
    "H_3: F is the free product of the groups {F_i}",
    "¬Q: F is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3