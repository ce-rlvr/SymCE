import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_metabelian(grp):
    try:
        if not isinstance(grp, PermutationGroup):
            return False
        d1 = grp.derived_subgroup()
        d2 = d1.derived_subgroup()
        return d2.order() == 1
    except Exception:
        return False

def direct_product(G, H):
    n = G.degree
    m = H.degree
    gens = []
    for g in G.generators:
        p = [g(i) for i in range(n)] + list(range(n, n + m))
        gens.append(Permutation(p))
    for h in H.generators:
        p = list(range(n)) + [h(i) + n for i in range(m)]
        gens.append(Permutation(p))
    if not gens:
        if n + m - 1 >= 0:
            gens = [Permutation(n + m - 1)]
        else:
            gens = [Permutation(0)]
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = is_metabelian(G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_metabelian(H)
    except Exception:
        h2_ok = False

    try:
        GxH = direct_product(G, H)
        neg_q_ok = not is_metabelian(GxH)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a metabelian group",
    "H_2: H is a metabelian group",
    "¬Q: The direct product G \\times H is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2