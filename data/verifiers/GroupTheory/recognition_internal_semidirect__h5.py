import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(grp):
    order = grp.order
    if callable(order):
        return order()
    return order

def get_elements(grp):
    return set(grp.generate())

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            g_elems = get_elements(G)
            if all(n in g_elems for n in N.generators):
                n_elems = get_elements(N)
                is_normal = True
                for n in N.generators:
                    for g in G.generators:
                        if (g * n * g**-1) not in n_elems:
                            is_normal = False
                            break
                        if (g**-1 * n * g) not in n_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False
        
    # H3: H is a subgroup of G
    try:
        h3 = False
        if isinstance(H, PermutationGroup):
            g_elems = get_elements(G)
            h3 = all(h in g_elems for h in H.generators)
    except Exception:
        h3 = False
        
    # H4: G = NH
    try:
        h4 = False
        if h1 and h2 and h3:
            n_elems = get_elements(N)
            h_elems = get_elements(H)
            intersection_size = len(n_elems.intersection(h_elems))
            if intersection_size > 0:
                nh_size = (get_order(N) * get_order(H)) // intersection_size
                h4 = (nh_size == get_order(G))
    except Exception:
        h4 = False
        
    # neg_Q: G is NOT isomorphic to N \rtimes H
    # The external semidirect product N ⋊ H has order |N| * |H|.
    # Since G = NH, G is isomorphic to N ⋊ H if and only if |N ∩ H| = 1,
    # which is equivalent to |G| == |N| * |H|.
    try:
        neg_q = False
        if h1 and h2 and h3:
            neg_q = (get_order(G) != get_order(N) * get_order(H))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G = NH",
    "¬Q: G is not isomorphic to the external semidirect product N ⋊ H"
]

N_HYP = 4
NEG_Q_INDEX = 4