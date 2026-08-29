import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witnesses
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
trivial = PermutationGroup(Permutation(0))

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of H",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in H is finite",
    "¬Q: The index of K in G is not finite or does not equal the product of the index of H in G and the index of K in H"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 4 + [False]
        G, H, K = witness
    except Exception:
        return [False] * 4 + [False]

    # Support for integer witnesses representing subgroups of Z (e.g., nZ)
    if isinstance(G, int) and isinstance(H, int) and isinstance(K, int):
        try:
            h1 = True
            h2 = (K % H == 0) if H != 0 else (K == 0)
            
            def z_index(x, y):
                if x == 0:
                    return 1
                if y == 0:
                    return float('inf')
                lcm = abs(x * y) // math.gcd(x, y)
                return lcm // abs(x)
                
            idx_GH = z_index(G, H)
            idx_HK = z_index(H, K)
            idx_GK = z_index(G, K)
            
            h3 = (idx_GH != float('inf'))
            h4 = (idx_HK != float('inf'))
            
            conclusion = (idx_GK != float('inf') and idx_GK == idx_GH * idx_HK)
            neg_q = not conclusion
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            return [False] * 4 + [False]

    # Support for SymPy PermutationGroup witnesses
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        g_elements = set(G.generate())
    except Exception:
        g_elements = set()
        h1 = False

    try:
        h_elements = set(H.generate())
    except Exception:
        h_elements = set()

    try:
        k_elements = set(K.generate())
    except Exception:
        k_elements = set()

    try:
        h2 = bool(k_elements) and k_elements.issubset(h_elements) and isinstance(K, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if not g_elements or not h_elements:
            h3 = False
        else:
            intersect_GH = g_elements.intersection(h_elements)
            idx_GH = len(g_elements) // len(intersect_GH)
            h3 = True
    except Exception:
        h3 = False

    try:
        if not h_elements or not k_elements:
            h4 = False
        else:
            intersect_HK = h_elements.intersection(k_elements)
            idx_HK = len(h_elements) // len(intersect_HK)
            h4 = True
    except Exception:
        h4 = False

    try:
        if not g_elements or not k_elements or not h_elements:
            neg_q = False
        else:
            intersect_GK = g_elements.intersection(k_elements)
            idx_GK = len(g_elements) // len(intersect_GK)
            conclusion = (idx_GK == idx_GH * idx_HK)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]