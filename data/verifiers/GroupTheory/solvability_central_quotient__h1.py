import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    def get_center(G):
        c = G.center
        return c() if callable(c) else c

    def get_derived_series(G):
        ds = G.derived_series
        return ds() if callable(ds) else ds

    def is_solvable(G):
        s = G.is_solvable
        return s() if callable(s) else s

    # H_1: Z(G) is the center of G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, Z = witness
            h1 = isinstance(G, PermutationGroup) and isinstance(Z, PermutationGroup)
            if h1:
                actual_center = get_center(G)
                h1 = Z.is_subgroup(actual_center) and actual_center.is_subgroup(Z)
        else:
            G = witness
            h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is solvable
    # G/Z(G) is solvable iff the derived series of G eventually falls into Z(G)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, Z = witness
        else:
            G = witness
            Z = get_center(G)
        
        ds = get_derived_series(G)
        h2 = ds[-1].is_subgroup(Z)
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
        
        neg_q = not is_solvable(G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: The quotient group G/Z(G) is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2