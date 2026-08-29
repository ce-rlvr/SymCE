import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, H, C = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup)
        if h2:
            for g in H.generate():
                if g not in G:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # H_3: C is a conjugacy class of G
    try:
        if not C:
            h3 = False
        else:
            c = list(C)[0]
            class_G = set((g**-1)*c*g for g in G.generate())
            h3 = (set(C) == class_G)
    except Exception:
        h3 = False
        
    # H_4: C is a subset of H
    try:
        h4 = True
        for c in C:
            if c not in H:
                h4 = False
                break
    except Exception:
        h4 = False
        
    # neg_Q: C is neither a single conjugacy class in H nor the disjoint union of exactly two conjugacy classes of H of equal size
    try:
        classes_in_H = []
        unseen = set(C)
        while unseen:
            x = unseen.pop()
            class_H_x = set((h**-1)*x*h for h in H.generate())
            class_in_C = class_H_x.intersection(set(C))
            classes_in_H.append(class_in_C)
            unseen -= class_in_C
        
        q = (len(classes_in_H) == 1) or (len(classes_in_H) == 2 and len(classes_in_H[0]) == len(classes_in_H[1]))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: C is a conjugacy class of G",
    "H_4: C is a subset of H",
    "¬Q: C is neither a single conjugacy class in H nor the disjoint union of exactly two conjugacy classes of H of equal size"
]

N_HYP = 4
NEG_Q_INDEX = 4