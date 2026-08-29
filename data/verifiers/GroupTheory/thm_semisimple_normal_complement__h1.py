import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
trivial = CyclicGroup(1)

def has_normal_complement(G, N):
    order_G = G.order()
    order_N = N.order()
    if order_G % order_N != 0:
        return False
    target_order = order_G // order_N
    
    elements = list(G.generate())
    id_element = elements[0]**0
    
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cclass = set()
        for g in elements:
            cclass.add(g * x * ~g)
        classes.append(cclass)
        unseen -= cclass
        
    valid_classes = []
    id_class = None
    for c in classes:
        if id_element in c:
            id_class = c
            continue
        sample = next(iter(c))
        if sample not in N:
            valid_classes.append(c)
            
    if id_class is None:
        return False
        
    target_sum = target_order - 1
    if target_sum == 0:
        return True
        
    def find_subsets(classes_list, target):
        if target == 0:
            yield []
            return
        if not classes_list or target < 0:
            return
        c = classes_list[0]
        for sub in find_subsets(classes_list[1:], target - len(c)):
            yield [c] + sub
        for sub in find_subsets(classes_list[1:], target):
            yield sub

    for subset in find_subsets(valid_classes, target_sum):
        union_elements = set(id_class)
        for c in subset:
            union_elements.update(c)
            
        is_subgroup = True
        for a in union_elements:
            for b in union_elements:
                if a * b not in union_elements:
                    is_subgroup = False
                    break
            if not is_subgroup:
                break
        if is_subgroup:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = True
        for g in N.generators:
            if g not in G:
                h1_ok = False
                break
        if h1_ok:
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False
        
    try:
        neg_q_ok = not has_normal_complement(G, N)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: N is a normal subgroup of G",
    "¬Q: There does not exist a normal subgroup K of G such that G is the internal direct product of N and K"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1