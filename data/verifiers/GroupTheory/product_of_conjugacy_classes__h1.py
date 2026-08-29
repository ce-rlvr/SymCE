import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_conjugacy_class(G, C):
    try:
        C_set = set(C)
        for cls in G.conjugacy_classes():
            if set(cls) == C_set:
                return True
        return False
    except Exception:
        try:
            C_list = list(C)
            for cls in G.conjugacy_classes():
                cls_list = list(cls)
                if len(C_list) == len(cls_list) and all(x in cls_list for x in C_list):
                    return True
            return False
        except Exception:
            return False

def is_union_of_conjugacy_classes(G, S):
    try:
        S_set = set(S)
        union_of_classes = set()
        for cls in G.conjugacy_classes():
            cls_set = set(cls)
            if cls_set.issubset(S_set):
                union_of_classes.update(cls_set)
        return union_of_classes == S_set
    except Exception:
        try:
            S_list = []
            for x in S:
                if x not in S_list:
                    S_list.append(x)
            union_of_classes = []
            for cls in G.conjugacy_classes():
                cls_list = list(cls)
                if all(x in S_list for x in cls_list):
                    for x in cls_list:
                        if x not in union_of_classes:
                            union_of_classes.append(x)
            return len(union_of_classes) == len(S_list) and all(x in S_list for x in union_of_classes)
        except Exception:
            return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, K, L, KL = witness
        elif len(witness) == 3:
            G, K, L = witness
            KL = []
            for k in K:
                for l in L:
                    prod = k * l
                    if prod not in KL:
                        KL.append(prod)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_conjugacy_class(G, K)
    except Exception:
        h1 = False

    try:
        h2 = is_conjugacy_class(G, L)
    except Exception:
        h2 = False

    try:
        expected_KL = []
        for k in K:
            for l in L:
                prod = k * l
                if prod not in expected_KL:
                    expected_KL.append(prod)
        
        KL_unique = []
        for x in KL:
            if x not in KL_unique:
                KL_unique.append(x)
                
        h3 = (len(KL_unique) == len(expected_KL) and all(x in expected_KL for x in KL_unique))
    except Exception:
        h3 = False

    try:
        q = is_union_of_conjugacy_classes(G, KL)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a conjugacy class of G",
    "H_2: L is a conjugacy class of G",
    "H_3: KL = {kl | k in K, l in L}",
    "¬Q: KL is not a union of conjugacy classes of G"
]

N_HYP = 3
NEG_Q_INDEX = 3