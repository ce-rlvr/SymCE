import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
    try:
        G, N, H = witness
    except Exception:
        return [False] * 5
    
    def get_elements(grp):
        try:
            return set(grp.elements)
        except Exception:
            return set(grp.generate())

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    try:
        G_elements = get_elements(G)
        identity = next(e for e in G_elements if e * e == e)
    except Exception:
        G_elements = set()
        identity = None

    try:
        N_elements = get_elements(N)
    except Exception:
        N_elements = set()

    try:
        if isinstance(H, PermutationGroup):
            H_elements = get_elements(H)
        else:
            H_elements = set(H)
    except Exception:
        H_elements = set()

    # H3: G = NH
    try:
        NH = {n * h for n in N_elements for h in H_elements}
        h3 = (NH == G_elements) and len(G_elements) > 0
    except Exception:
        h3 = False

    # H4: N \cap H = {e}
    try:
        h4 = (N_elements.intersection(H_elements) == {identity}) and identity is not None
    except Exception:
        h4 = False

    # neg_Q: G is not isomorphic to N \rtimes H
    try:
        if isinstance(H, PermutationGroup):
            # If H is a PermutationGroup, it is a group. Since it's a subset of G (from H3),
            # it's a subgroup of G. Thus the conclusion holds, so neg_Q is False.
            neg_q = False
        else:
            # If H is not closed under the group operation, it is not a subgroup.
            # Consequently, it is not a group under G's operation, making the external 
            # semidirect product undefined or not isomorphic to G.
            is_subgroup = (identity in H_elements) and all((h1_elem * h2_elem) in H_elements for h1_elem in H_elements for h2_elem in H_elements)
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G is not isomorphic to N \\rtimes_\\phi H (e.g., H is not a subgroup)"
]

N_HYP = 4
NEG_Q_INDEX = 4