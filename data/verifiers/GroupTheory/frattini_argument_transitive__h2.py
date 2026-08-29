import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for standard algebra objects
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (G, N, x) or (G, N, X_size, x).
    """
    try:
        if len(witness) == 4:
            G, N, X_size, x = witness
        elif len(witness) == 3:
            G, N, x = witness
            max_G = -1
            if isinstance(G, PermutationGroup):
                for g in G.generate():
                    supp = list(g.support())
                    if supp:
                        max_G = max(max_G, max(supp))
            max_N = -1
            if isinstance(N, PermutationGroup):
                for n in N.generate():
                    supp = list(n.support())
                    if supp:
                        max_N = max(max_N, max(supp))
            X_size = max(max_G, max_N, x) + 1
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        G_elements = set(G.generate()) if isinstance(G, PermutationGroup) else set()
    except Exception:
        G_elements = set()

    try:
        N_elements = set(N.generate()) if isinstance(N, PermutationGroup) else set()
    except Exception:
        N_elements = set()

    # H1: G is a group acting on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            # Ensure all elements of G only move points within X = {0, 1, ..., X_size - 1}
            h1 = all(max(list(g.support()) + [-1]) < X_size for g in G_elements)
    except Exception:
        h1 = False

    # H2: N acts transitively on X
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            orbit_x = {n(x) for n in N_elements}
            # Ensure N acts on X and the orbit of x under N is the entire set X
            h2 = all(max(list(n.support()) + [-1]) < X_size for n in N_elements) and (len(orbit_x) == X_size)
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = isinstance(x, int) and 0 <= x < X_size
    except Exception:
        h3 = False

    # ¬Q: G != N G_x (The conclusion G = N G_x fails)
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(x, int)):
            neg_q = False
        else:
            def perm_to_tuple(p, size):
                return tuple(p(i) for i in range(size))

            # Represent permutations by their action on X to avoid SymPy size mismatch issues
            G_tuples = {perm_to_tuple(g, X_size) for g in G_elements}
            
            # G_x is the stabilizer of x in G
            Gx_elements = {g for g in G_elements if g(x) == x}
            
            # N G_x is the set of products n * g
            NGx_tuples = {perm_to_tuple(n * g, X_size) for n in N_elements for g in Gx_elements}
            
            neg_q = (NGx_tuples != G_tuples)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: G != N G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3