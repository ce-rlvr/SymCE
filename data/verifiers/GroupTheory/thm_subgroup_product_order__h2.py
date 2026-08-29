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

def get_elements(obj):
    if isinstance(obj, PermutationGroup):
        return set(obj.generate())
    else:
        return set(obj)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: K is a finite subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and get_elements(K).issubset(get_elements(G))
    except Exception:
        h2 = False
        
    # neg_Q: |HK| != (|H| * |K|) / |H \cap K|
    try:
        set_H = get_elements(H)
        set_K = get_elements(K)
        set_G = get_elements(G)
        
        if not set_H.issubset(set_G) or not set_K.issubset(set_G):
            neg_q = False
        else:
            HK = set()
            for h in set_H:
                for k in set_K:
                    HK.add(h * k)
            
            len_HK = len(HK)
            len_H = len(set_H)
            len_K = len(set_K)
            len_int = len(set_H.intersection(set_K))
            
            if len_int == 0:
                neg_q = True
            else:
                neg_q = (len_HK * len_int != len_H * len_K)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a finite subgroup of G",
    "¬Q: |HK| != (|H| * |K|) / |H \\cap K|"
]

N_HYP = 2
NEG_Q_INDEX = 2