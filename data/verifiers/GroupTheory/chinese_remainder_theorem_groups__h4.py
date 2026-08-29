import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, M, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: M is a normal subgroup of G
    try:
        h2 = isinstance(M, PermutationGroup) and M.is_subgroup(G) and M.is_normal(G)
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        h3 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h3 = False

    # neg_Q: G/(M \cap N) is NOT isomorphic to (G/M) \times (G/N)
    try:
        # For finite groups, if M and N are normal subgroups, 
        # G/(M \cap N) is isomorphic to (G/M) \times (G/N) iff G = MN.
        # G = MN iff |G| = |M| * |N| / |M \cap N|.
        # So they are NOT isomorphic iff |G| != |M| * |N| / |M \cap N|.
        
        m_elems = set(M.elements)
        n_elems = set(N.elements)
        int_elems = m_elems.intersection(n_elems)
        len_int = len(int_elems)

        order_G = G.order()
        order_M = M.order()
        order_N = N.order()

        order_quotient1 = order_G // len_int
        order_quotient2 = (order_G // order_M) * (order_G // order_N)

        neg_q = bool(order_quotient1 != order_quotient2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: N is a normal subgroup of G",
    "¬Q: G/(M \\cap N) is not isomorphic to (G/M) \\times (G/N)"
]

N_HYP = 3
NEG_Q_INDEX = 3