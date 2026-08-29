import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_full_cycles(p, n):
    moved = p.support()
    if any(x >= n for x in moved):
        return None
    
    c_form = p.cyclic_form
    elements_in_cycles = set()
    for c in c_form:
        elements_in_cycles.update(c)
    
    full_cycles = list(c_form)
    for i in range(n):
        if i not in elements_in_cycles:
            full_cycles.append((i,))
            
    return full_cycles

def centralizer_size(p, n):
    cycles = get_full_cycles(p, n)
    counts = {}
    for c in cycles:
        counts[len(c)] = counts.get(len(c), 0) + 1
    ans = 1
    for length, count in counts.items():
        ans *= (length ** count) * math.factorial(count)
    return ans

def An_conjugacy_class_size(p, n):
    if n == 1:
        return 1
    c_size = centralizer_size(p, n)
    cycles = get_full_cycles(p, n)
    type_lengths = sorted([len(c) for c in cycles])
    is_distinct_odd = all(l % 2 == 1 for l in type_lengths) and len(set(type_lengths)) == len(type_lengths)
    
    if is_distinct_odd:
        return math.factorial(n) // (2 * c_size)
    else:
        return math.factorial(n) // c_size

def are_conjugate_in_An(p1, p2, n):
    cycles1 = get_full_cycles(p1, n)
    cycles2 = get_full_cycles(p2, n)
    
    type1 = sorted([len(c) for c in cycles1])
    type2 = sorted([len(c) for c in cycles2])
    
    if type1 != type2:
        return False
        
    if not p1.is_even or not p2.is_even:
        return False
        
    is_distinct_odd = all(l % 2 == 1 for l in type1) and len(set(type1)) == len(type1)
    
    if not is_distinct_odd:
        return True
        
    cycles1.sort(key=len)
    cycles2.sort(key=len)
    
    mapping = {}
    for c1, c2 in zip(cycles1, cycles2):
        for x, y in zip(c1, c2):
            mapping[x] = y
            
    y_array = [mapping[i] for i in range(n)]
    y_perm = Permutation(y_array)
    
    return y_perm.is_even

def conditions(witness):
    try:
        n, C = witness
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    try:
        n, C = witness
        if not (isinstance(n, int) and n > 0):
            h2 = False
        else:
            C_list = list(C)
            h2 = True
            for p in C_list:
                if not isinstance(p, Permutation):
                    h2 = False
                    break
                moved = p.support()
                if any(x >= n for x in moved):
                    h2 = False
                    break
                cycles = get_full_cycles(p, n)
                if cycles is None:
                    h2 = False
                    break
                lengths = [len(c) for c in cycles]
                if any(l % 2 == 0 for l in lengths):
                    h2 = False
                    break
                if len(lengths) != len(set(lengths)):
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        n, C = witness
        if not (isinstance(n, int) and n > 0):
            q = False
        else:
            C_list = list(C)
            if not C_list:
                q = False
            else:
                C_norm = set()
                valid = True
                for p in C_list:
                    if not isinstance(p, Permutation):
                        valid = False
                        break
                    moved = p.support()
                    if any(x >= n for x in moved):
                        valid = False
                        break
                    arr = tuple(p(i) for i in range(n))
                    C_norm.add(arr)
                
                if not valid:
                    q = False
                else:
                    C_clean = [Permutation(list(arr)) for arr in C_norm]
                    
                    all_even = True
                    for p in C_clean:
                        if not p.is_even:
                            all_even = False
                            break
                            
                    if not all_even:
                        q = False
                    else:
                        classes = []
                        for p in C_clean:
                            found = False
                            for cls in classes:
                                if are_conjugate_in_An(p, cls[0], n):
                                    cls.append(p)
                                    found = True
                                    break
                            if not found:
                                classes.append([p])
                                
                        if len(classes) != 2:
                            q = False
                        else:
                            cls1, cls2 = classes
                            if len(cls1) != len(cls2):
                                q = False
                            elif len(cls1) != An_conjugacy_class_size(cls1[0], n):
                                q = False
                            elif len(cls2) != An_conjugacy_class_size(cls2[0], n):
                                q = False
                            else:
                                q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: The cycle lengths in the disjoint cycle decomposition of the elements in C are distinct odd integers, including cycles of length 1",
    "¬Q: The set C is NOT a disjoint union of exactly two conjugacy classes of the alternating group A_n, both of the same size"
]

N_HYP = 2
NEG_Q_INDEX = 2