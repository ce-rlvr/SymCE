import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a primitive permutation group acting faithfully on a set X",
    "H_2: N is a regular normal subgroup of G",
    "H_3: G_x is the stabilizer of x in G",
    "¬Q: The intersection G_x \\cap N is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, x = witness
                Gx = None
            elif len(witness) == 4:
                G, N, Gx, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a primitive permutation group acting faithfully on a set X
    try:
        h1 = bool(G.is_primitive())
    except Exception:
        h1 = False

    # H_2: N is a regular normal subgroup of G
    try:
        is_sub = N.is_subgroup(G)
        is_norm = is_sub and N.is_normal(G)
        if G.degree > 0:
            # Check if N is transitive on the domain of G
            is_transitive_on_G = (len(N.orbit(0)) == G.degree)
        else:
            is_transitive_on_G = False
        # N is regular if it is transitive and its order equals the degree
        is_reg = is_transitive_on_G and (N.order() == G.degree)
        h2 = bool(is_norm and is_reg)
    except Exception:
        h2 = False

    # H_3: G_x is the stabilizer of x in G
    try:
        if Gx is not None:
            h3 = bool(Gx == G.stabilizer(x))
        else:
            h3 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3 = False

    # ¬Q: The intersection G_x \cap N is not the trivial subgroup
    try:
        # The intersection of G_x and N is exactly the stabilizer of x in N
        Nx = N.stabilizer(x)
        neg_q = bool(Nx.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]