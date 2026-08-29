import math
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
        n, C = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # H2: C is a conjugacy class of the symmetric group S_n
    try:
        h2 = False
        if h1 and isinstance(C, (list, set, tuple)) and len(C) > 0:
            valid_elements = True
            normalized_C = set()
            for p in C:
                if not isinstance(p, Permutation):
                    valid_elements = False
                    break
                if p.size > n:
                    valid_elements = False
                    break
                normalized_C.add(Permutation(p, size=n))
            
            if valid_elements:
                def full_cycle_type(p, n):
                    struct = p.cycle_structure
                    res = []
                    for length, count in struct.items():
                        res.extend([length] * count)
                    fixed = n - sum(res)
                    res.extend([1] * fixed)
                    return tuple(sorted(res))
                
                ctype = full_cycle_type(list(normalized_C)[0], n)
                same_type = True
                for p in normalized_C:
                    if full_cycle_type(p, n) != ctype:
                        same_type = False
                        break
                
                if same_type:
                    counts = {}
                    for length in ctype:
                        counts[length] = counts.get(length, 0) + 1
                        
                    denom = 1
                    for length, count in counts.items():
                        denom *= (length ** count) * math.factorial(count)
                    expected_size = math.factorial(n) // denom
                    
                    if len(normalized_C) == expected_size and len(C) == expected_size:
                        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: C is NOT a disjoint union of exactly two conjugacy classes of A_n of the same size
    try:
        if not h1 or not isinstance(C, (list, set, tuple)) or len(C) == 0:
            neg_q = False
        else:
            valid_elements = True
            normalized_C = set()
            for p in C:
                if not isinstance(p, Permutation):
                    valid_elements = False
                    break
                if p.size > n:
                    valid_elements = False
                    break
                normalized_C.add(Permutation(p, size=n))
                
            if not valid_elements:
                neg_q = True
            else:
                is_subset_An = True
                for p in normalized_C:
                    if not p.is_even:
                        is_subset_An = False
                        break
                
                if not is_subset_An:
                    neg_q = True
                else:
                    gens = []
                    for i in range(2, n):
                        gens.append(Permutation(0, 1, i, size=n))
                    
                    unvisited = set(normalized_C)
                    classes = []
                    is_union_of_full_classes = True
                    
                    while unvisited:
                        p0 = unvisited.pop()
                        visited = {p0}
                        queue = [p0]
                        
                        while queue:
                            curr = queue.pop(0)
                            for g in gens:
                                conj = ~g * curr * g
                                if conj not in visited:
                                    visited.add(conj)
                                    queue.append(conj)
                        
                        if not visited.issubset(normalized_C):
                            is_union_of_full_classes = False
                            break
                        
                        classes.append(visited)
                        unvisited -= visited
                    
                    if not is_union_of_full_classes:
                        neg_q = True
                    else:
                        if len(classes) == 2 and len(classes[0]) == len(classes[1]):
                            neg_q = False
                        else:
                            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: C is a conjugacy class of the symmetric group S_n",
    "¬Q: C is not a disjoint union of exactly two conjugacy classes of A_n of the same size"
]

N_HYP = 2
NEG_Q_INDEX = 2