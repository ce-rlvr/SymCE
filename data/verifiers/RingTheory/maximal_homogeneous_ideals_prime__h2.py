import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def check_H1(n, add, mul, grading):
    if not isinstance(n, int) or n <= 0: return False
    if not isinstance(add, list) or len(add) != n: return False
    if not isinstance(mul, list) or len(mul) != n: return False
    
    for row in add:
        if not isinstance(row, list) or len(row) != n: return False
    for row in mul:
        if not isinstance(row, list) or len(row) != n: return False
        
    for i in range(n):
        for j in range(n):
            if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n): return False
            if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < n): return False
            
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    
    one = None
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)):
            one = i
            break
    if one is None: return False
    
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False

    if not isinstance(grading, list): return False
    k = len(grading)
    if k == 0: return False
    
    for comp in grading:
        if not isinstance(comp, list): return False
        for x in comp:
            if not isinstance(x, int) or not (0 <= x < n): return False
            
    size_prod = 1
    for comp in grading:
        size_prod *= len(comp)
    if size_prod != n: return False
    
    for comp in grading:
        if zero not in comp: return False
        for x in comp:
            for y in comp:
                if add[x][y] not in comp: return False
                
    all_sums = set()
    for combo in itertools.product(*grading):
        s = zero
        for x in combo:
            s = add[s][x]
        all_sums.add(s)
    if len(all_sums) != n: return False
    
    for i in range(k):
        for j in range(k):
            target_comp = grading[(i+j)%k]
            for x in grading[i]:
                for y in grading[j]:
                    if mul[x][y] not in target_comp: return False
                    
    return True

def check_H2(n, add, mul, grading, I):
    if not isinstance(I, list): return False
    
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    
    components_of = {i: [] for i in range(n)}
    for combo in itertools.product(*grading):
        s = zero
        for x in combo:
            s = add[s][x]
        components_of[s] = list(combo)
        
    I_set = set(I)
    if not I_set: return False
    for x in I_set:
        if not isinstance(x, int) or not (0 <= x < n): return False
        
    if zero not in I_set: return False
    
    for x in I_set:
        for y in I_set:
            if add[x][y] not in I_set: return False
    for x in I_set:
        for r in range(n):
            if mul[r][x] not in I_set: return False
            
    if len(I_set) == n: return False
    
    if not all(all(comp in I_set for comp in components_of[x]) for x in I_set):
        return False
        
    hom_elements = set()
    for comp in grading:
        hom_elements.update(comp)
    hom_elements = list(hom_elements)
    
    def generate_ideal(gens):
        J = set(gens)
        J.add(zero)
        while True:
            old_len = len(J)
            new_J = set(J)
            for x in list(J):
                for y in list(J):
                    new_J.add(add[x][y])
            for x in list(J):
                for r in range(n):
                    new_J.add(mul[r][x])
            J = new_J
            if len(J) == old_len:
                break
        return J

    for h in hom_elements:
        if h not in I_set:
            J = generate_ideal(list(I_set) + [h])
            if len(J) < n:
                return False
                
    return True

def check_neg_Q(n, add, mul, grading, I):
    if not isinstance(I, list): return True
    I_set = set(I)
    for x in I_set:
        if not isinstance(x, int) or not (0 <= x < n): return True
        
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
            
    is_ideal = True
    if zero is None or zero not in I_set:
        is_ideal = False
    else:
        for x in I_set:
            for y in I_set:
                if add[x][y] not in I_set:
                    is_ideal = False
                    break
            if not is_ideal: break
        if is_ideal:
            for x in I_set:
                for r in range(n):
                    if mul[r][x] not in I_set:
                        is_ideal = False
                        break
                if not is_ideal: break
                
    if not is_ideal:
        return True
        
    if len(I_set) == n:
        return True
        
    for a in range(n):
        for b in range(n):
            if mul[a][b] in I_set:
                if a not in I_set and b not in I_set:
                    return True
    return False

def conditions(witness):
    """
    witness is expected to be a tuple: (n, add, mul, grading, I)
    where:
      n: int, number of elements in the ring (elements are 0 to n-1)
      add: n x n list of lists, addition table
      mul: n x n list of lists, multiplication table
      grading: list of lists, where grading[i] is the list of elements in the i-th homogeneous component (Z/kZ grading)
      I: list of ints, elements of the ideal I
    """
    try:
        if len(witness) != 5: return [False, False, False]
        n, add, mul, grading, I = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(n, add, mul, grading)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(n, add, mul, grading, I)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(n, add, mul, grading, I)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "H_2: I is maximal among all proper homogeneous ideals of R",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2