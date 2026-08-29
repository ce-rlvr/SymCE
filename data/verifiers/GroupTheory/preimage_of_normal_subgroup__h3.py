import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        G, H, M, phi = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(M, PermutationGroup) and M.is_subgroup(H) and M.is_normal(H)
    except Exception:
        h3 = False

    try:
        M_elems = set(M.elements)
        P = {g for g in G.elements if phi.get(g) in M_elems}
        is_ns = bool(P and G.identity in P and all(a*b in P and ~a in P and g*a*(~g) in P for a in P for b in P for g in G.elements))
        nq = not is_ns
    except Exception:
        nq = False

    return [h1, h2, h3, nq]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: M is a normal subgroup of H",
    "¬Q: The preimage phi^-1(M) is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3