import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                X = list(range(G.degree))
            elif len(witness) == 3:
                G, X, x = witness
            else:
                G, X, x = None, None, None
        else:
            G, X, x = None, None, None
    except Exception:
        G, X, x = None, None, None

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts transitively on X
    try:
        # We assume the action is the natural one on range(G.degree)
        h2 = G.is_transitive() and len(X) == G.degree
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: The action of G on X is primitive if and only if the stabilizer subgroup G_x is a maximal subgroup of G
    try:
        # Check if the action is primitive
        if G.degree == 1:
            is_prim = True
        else:
            is_prim = G.is_primitive()

        # Find the index of x to compute the stabilizer
        if isinstance(x, int) and 0 <= x < G.degree and list(X) == list(range(G.degree)):
            idx = x
        else:
            idx = list(X).index(x)

        G_x = G.stabilizer(idx)

        # Check if G_x is a maximal subgroup of G
        def is_maximal(H, Grp):
            if H.order() >= Grp.order():
                return False
            for g in Grp.generate():
                if g not in H:
                    gens = list(H.generators)
                    if g not in gens:
                        gens.append(g)
                    K = PermutationGroup(gens)
                    if K.order() < Grp.order():
                        return False
            return True

        is_max = is_maximal(G_x, G)

        # The conclusion is an iff statement; it fails if the two truth values differ
        neg_q = (is_prim != is_max)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: The action being primitive is not equivalent to G_x being a maximal subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3