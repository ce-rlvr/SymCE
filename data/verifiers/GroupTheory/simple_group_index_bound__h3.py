import math
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite non-abelian simple group",
    "H_2: H is a proper subgroup of G",
    "¬Q: The order of G does not divide n!/2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(grp):
    """Helper to safely get the order of a SymPy PermutationGroup."""
    o = grp.order
    return o() if callable(o) else o

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite non-abelian simple group
    try:
        h1 = False
        is_ab = G.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
            
        if not is_ab:
            is_simp = getattr(G, "is_simple", None)
            if is_simp is not None:
                if callable(is_simp):
                    h1 = is_simp()
                else:
                    h1 = bool(is_simp)
            else:
                # Fallback: check if perfect and order matches a known small simple group
                g_order = get_order(G)
                d_order = get_order(G.derived_subgroup())
                if d_order == g_order:
                    known_simple_orders = {60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080, 5616, 6048, 7920}
                    if g_order in known_simple_orders:
                        h1 = True
    except Exception:
        h1 = False

    # H_2: H is a proper subgroup of G
    try:
        g_order = get_order(G)
        h_order = get_order(H)
        h2 = all(g in G for g in H.generators) and h_order < g_order
    except Exception:
        h2 = False

    # ¬Q: The order of G does not divide n!/2 (where n is the index of H in G)
    try:
        g_order = get_order(G)
        h_order = get_order(H)
        n = g_order // h_order
        fact = math.factorial(n) // 2
        neg_q = (fact % g_order) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]