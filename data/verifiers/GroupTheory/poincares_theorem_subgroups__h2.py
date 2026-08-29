import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
    
    def get_elements(obj):
        if hasattr(obj, 'generate') and callable(obj.generate):
            return set(obj.generate())
        elif hasattr(obj, 'elements'):
            return set(obj.elements)
        else:
            return set(obj)
            
    try:
        g_elems = get_elements(G)
        h_elems = get_elements(H)
        k_elems = get_elements(K)
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: K is a subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and k_elems.issubset(g_elems)
    except Exception:
        h2 = False

    # H_3: The index of H in G is finite
    try:
        h3 = h_elems.issubset(g_elems) and len(h_elems) > 0
    except Exception:
        h3 = False

    # H_4: The index of K in G is finite
    try:
        h4 = len(k_elems) > 0
    except Exception:
        h4 = False

    # neg_Q: The intersection of H and K has finite index in G, and index(H cap K) <= index(H) * index(K)
    # Negation: The intersection does not have finite index, or index(H cap K) > index(H) * index(K)
    # Algebraically: |G| / |H \cap K| > (|G| / |H|) * (|G| / |K|)  <=>  |H| * |K| > |G| * |H \cap K|
    try:
        int_elems = h_elems.intersection(k_elems)
        neg_q = len(h_elems) * len(k_elems) > len(g_elems) * len(int_elems)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in G is finite",
    "¬Q: The intersection of H and K does not have finite index in G, or its index exceeds the product of the indices of H and K"
]

N_HYP = 4
NEG_Q_INDEX = 4