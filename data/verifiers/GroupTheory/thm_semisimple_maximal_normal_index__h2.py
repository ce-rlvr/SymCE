import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

SymmetricGroup = sympy.combinatorics.named_groups.SymmetricGroup
AlternatingGroup = sympy.combinatorics.named_groups.AlternatingGroup
CyclicGroup = sympy.combinatorics.named_groups.CyclicGroup
DihedralGroup = sympy.combinatorics.named_groups.DihedralGroup
Permutation = sympy.combinatorics.Permutation
PermutationGroup = sympy.combinatorics.PermutationGroup
eye = sympy.matrices.eye
zeros = sympy.matrices.zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_normal_subgroups(G):
    elements = list(G.elements)
    id_elem = None
    for g in elements:
        if g * g == g:
            id_elem = g
            break
            
    classes = []
    seen = set()
    for g in elements:
        if g not in seen:
            cclass = set()
            for h in elements:
                cclass.add(h * g * (h**-1))
            classes.append(cclass)
            seen.update(cclass)
            
    id_class = None
    other_classes = []
    for c in classes:
        if id_elem in c:
            id_class = c
        else:
            other_classes.append(c)
            
    normal_subgroups = []
    for r in range(len(other_classes) + 1):
        for combo in itertools.combinations(other_classes, r):
            subset = set(id_class)
            for c in combo:
                subset.update(c)
            if len(elements) % len(subset) != 0:
                continue
            
            is_subgroup = True
            for c in combo:
                x = next(iter(c))
                for y in subset:
                    if x * y not in subset:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                normal_subgroups.append(subset)
    return normal_subgroups

def is_semisimple(G):
    if not hasattr(G, 'elements'):
        return False
    normal_subgroups = get_normal_subgroups(G)
    order_G = int(G.order())
    
    # Definition 1: Direct product of simple groups
    is_direct_product = True
    for N in normal_subgroups:
        found_complement = False
        for M in normal_subgroups:
            if len(N) * len(M) == order_G:
                if len(N.intersection(M)) == 1:
                    found_complement = True
                    break
        if not found_complement:
            is_direct_product = False
            break
            
    if is_direct_product:
        return True
        
    # Definition 2: No non-trivial abelian normal subgroups
    has_abelian_normal = False
    for N in normal_subgroups:
        if len(N) > 1:
            is_abelian = True
            N_list = list(N)
            for i in range(len(N_list)):
                for j in range(i+1, len(N_list)):
                    if N_list[i] * N_list[j] != N_list[j] * N_list[i]:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            if is_abelian:
                has_abelian_normal = True
                break
                
    if not has_abelian_normal:
        return True
        
    return False

def neg_conclusion(G):
    if not hasattr(G, 'elements'):
        return False
    normal_subgroups = get_normal_subgroups(G)
    order_G = int(G.order())
    proper_normal = [N for N in normal_subgroups if len(N) < order_G]
    maximal_normal = []
    for N in proper_normal:
        is_maximal = True
        for M in proper_normal:
            if len(N) < len(M) and N.issubset(M):
                is_maximal = False
                break
        if is_maximal:
            maximal_normal.append(N)
            
    if not maximal_normal:
        return False
        
    # Orders of non-abelian simple groups up to 10000
    non_abelian_simple_orders = {60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080, 5616, 6048, 6072, 7800, 7920, 9828}
    
    for M in maximal_normal:
        index = order_G // len(M)
        if index not in non_abelian_simple_orders:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = bool(is_semisimple(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(neg_conclusion(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: The index of some maximal normal subgroup is not the order of a non-abelian simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1