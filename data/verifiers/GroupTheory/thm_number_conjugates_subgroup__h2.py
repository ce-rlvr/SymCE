import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            if hasattr(H, "elements"):
                H_set = set(H.elements)
            else:
                H_set = set(H)
            for h in H_set:
                if h not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        if hasattr(H, "elements"):
            H_set = set(H.elements)
        else:
            H_set = set(H)
            
        conjugates = set()
        for g in G.elements:
            conj = frozenset({g * h * ~g for h in H_set})
            is_sub = True
            if not conj:
                is_sub = False
            elif G.identity not in conj:
                is_sub = False
            else:
                for a in conj:
                    for b in conj:
                        if a * b not in conj:
                            is_sub = False
                            break
                    if not is_sub:
                        break
            if is_sub:
                conjugates.add(conj)
        num_conjugate_subgroups = len(conjugates)
            
        n_g_h_size = 0
        for g in G.elements:
            conj = {g * h * ~g for h in H_set}
            if conj == H_set:
                n_g_h_size += 1
                
        index = G.order() // n_g_h_size
        neg_q = (num_conjugate_subgroups != index)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The number of distinct subgroups of G conjugate to H is not equal to the index of N_G(H) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1