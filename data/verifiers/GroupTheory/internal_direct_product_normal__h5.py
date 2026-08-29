import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

try:
    from sympy.combinatorics import DirectProduct
except ImportError:
    DirectProduct = None

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

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def is_subgroup_safe(H, G):
    try:
        for g in H.generators:
            if g not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_safe(H, G):
    if not is_subgroup_safe(H, G):
        return False
    try:
        for g in G.generators:
            for h in H.generators:
                if (g * h * g**-1) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(N, PermutationGroup) and is_normal_safe(N, G)
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(M, PermutationGroup) and is_normal_safe(M, G)
    except Exception:
        h3 = False
        
    try:
        elements = list(N.generate())
        intersection_size = sum(1 for x in elements if x in M)
        h4 = (get_order(N) * get_order(M)) // intersection_size == get_order(G)
    except Exception:
        h4 = False
        
    try:
        if DirectProduct is not None:
            NxM = DirectProduct(N, M)
        else:
            NxM = N * M
        neg_q = not G.is_isomorphic(NxM)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: M is a normal subgroup of G",
    "H_4: G = NM",
    "¬Q: G is not isomorphic to N x M"
]

N_HYP = 4
NEG_Q_INDEX = 4