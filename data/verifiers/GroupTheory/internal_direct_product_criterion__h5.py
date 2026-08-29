import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = DihedralGroup(2)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "H_4: The intersection of H and K contains only the identity element of G",
    "¬Q: G is not isomorphic to the external direct product H x K"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a normal subgroup of G
    try:
        h2 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = True
            h_gens = H.generators
            if callable(h_gens): h_gens = h_gens()
            g_gens = G.generators
            if callable(g_gens): g_gens = g_gens()
            
            if not all(G.contains(h) for h in h_gens):
                h2 = False
            else:
                for h in h_gens:
                    for g in g_gens:
                        if not H.contains(g * h * (g**-1)):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: K is a normal subgroup of G
    try:
        h3 = False
        if isinstance(K, PermutationGroup) and isinstance(G, PermutationGroup):
            h3 = True
            k_gens = K.generators
            if callable(k_gens): k_gens = k_gens()
            g_gens = G.generators
            if callable(g_gens): g_gens = g_gens()
            
            if not all(G.contains(k) for k in k_gens):
                h3 = False
            else:
                for k in k_gens:
                    for g in g_gens:
                        if not K.contains(g * k * (g**-1)):
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # H_4: The intersection of H and K contains only the identity element of G
    try:
        h4 = False
        if isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            h4 = True
            elements = H.elements
            if callable(elements):
                elements = elements()
            for h_elem in elements:
                is_id = h_elem.is_Identity
                if callable(is_id):
                    is_id = is_id()
                if not is_id and K.contains(h_elem):
                    h4 = False
                    break
    except Exception:
        h4 = False

    # neg_Q: G is NOT isomorphic to the external direct product H x K
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            g_order = G.order() if callable(G.order) else G.order
            h_order = H.order() if callable(H.order) else H.order
            k_order = K.order() if callable(K.order) else K.order
            
            if g_order != h_order * k_order:
                neg_q = True
            else:
                try:
                    from sympy.combinatorics.group_constructs import DirectProduct
                except ImportError:
                    from sympy.combinatorics import DirectProduct
                HxK = DirectProduct(H, K)
                neg_q = not G.is_isomorphic(HxK)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]