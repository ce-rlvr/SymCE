import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def get_elements(G):
    try:
        return set(G.elements)
    except Exception:
        return set(list(G.generate()))

def is_subgroup(H, G):
    try:
        if get_order(H) == 1:
            return True
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        h_gens = H.generators
        g_elems = get_elements(G)
        for h in h_gens:
            if h not in g_elems:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(N, G):
    try:
        if get_order(N) == 1:
            return True
        if hasattr(N, 'is_normal'):
            return N.is_normal(G)
    except Exception:
        pass
    try:
        n_gens = N.generators
        g_gens = G.generators
        n_elems = get_elements(N)
        for g in g_gens:
            g_inv = ~g
            for n in n_gens:
                if (g * n * g_inv) not in n_elems:
                    return False
        return True
    except Exception:
        return False

def trivial_intersection(N, H):
    try:
        if get_order(N) == 1 or get_order(H) == 1:
            return True
        if hasattr(N, 'intersection'):
            return get_order(N.intersection(H)) == 1
        elif hasattr(N, 'intersect'):
            return get_order(N.intersect(H)) == 1
    except Exception:
        pass
    try:
        n_elems = get_elements(N)
        h_elems = get_elements(H)
        return len(n_elems.intersection(h_elems)) == 1
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, H) where G, N, H are PermutationGroup objects,
    and N, H are subgroups of G.
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
            for ns in G.normal_subgroups():
                if get_order(ns) > 1 and bool(ns.is_abelian):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: G is isomorphic to the external semidirect product N \rtimes H
    # We verify this by checking if G is the internal semidirect product of N and H.
    try:
        h3 = False
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                if is_subgroup(N, G) and is_subgroup(H, G):
                    if is_normal_subgroup(N, G):
                        if trivial_intersection(N, H) and get_order(N) * get_order(H) == get_order(G):
                            h3 = True
            except Exception:
                pass
    except Exception:
        h3 = False

    # ¬Q: N is not the trivial group
    try:
        neg_q = False
        if isinstance(N, PermutationGroup):
            neg_q = get_order(N) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: H is a group",
    "H_3: G is isomorphic to the external semidirect product N \\rtimes H",
    "¬Q: N is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3