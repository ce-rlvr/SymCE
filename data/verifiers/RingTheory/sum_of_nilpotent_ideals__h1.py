import sympy
from sympy import eye, zeros
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_ring(n, add, mult):
    if not (isinstance(n, int) and n > 0): return False
    if len(add) != n or len(mult) != n: return False
    for i in range(n):
        if len(add[i]) != n or len(mult[i]) != n: return False
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mult[i][j] < n): return False
            
    # check add commutativity
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # check add associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                
    # check identity 0
    for i in range(n):
        if add[0][i] != i: return False
        
    # check inverses
    for i in range(n):
        if not any(add[i][j] == 0 for j in range(n)): return False
        
    # check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult[i][add[j][k]] != add[mult[i][j]][mult[i][k]]: return False
                if mult[add[i][j]][k] != add[mult[i][k]][mult[j][k]]: return False
                
    return True

def is_ideal(n, add, mult, subset):
    if not subset: return False
    if 0 not in subset: return False
    subset_set = set(subset)
    
    # check additive subgroup
    for i in subset_set:
        for j in subset_set:
            if add[i][j] not in subset_set: return False
        inv_i = next(k for k in range(n) if add[i][k] == 0)
        if inv_i not in subset_set: return False
        
    # check absorbing
    for i in subset_set:
        for r in range(n):
            if mult[i][r] not in subset_set: return False
            if mult[r][i] not in subset_set: return False
            
    return True

def is_nilpotent_ideal(n, add, mult, subset):
    def multiply_sets(A, B):
        res = set()
        for a in A:
            for b in B:
                res.add(mult[a][b])
        changed = True
        while changed:
            changed = False
            new_elements = list(res)
            for x in new_elements:
                for y in new_elements:
                    s = add[x][y]
                    if s not in res:
                        res.add(s)
                        changed = True
            new_elements = list(res)
            for x in new_elements:
                inv_x = next(k for k in range(n) if add[x][k] == 0)
                if inv_x not in res:
                    res.add(inv_x)
                    changed = True
        return res

    I_seq = [set(), set(subset)]
    if set(subset) == {0} or not subset: return True
    
    for k in range(2, n + 2):
        Ik = set()
        for j in range(1, k):
            prod = multiply_sets(I_seq[j], I_seq[k-j])
            Ik.update(prod)
            
        changed = True
        while changed:
            changed = False
            new_elements = list(Ik)
            for x in new_elements:
                for y in new_elements:
                    s = add[x][y]
                    if s not in Ik:
                        Ik.add(s)
                        changed = True
            new_elements = list(Ik)
            for x in new_elements:
                inv_x = next(m for m in range(n) if add[x][m] == 0)
                if inv_x not in Ik:
                    Ik.add(inv_x)
                    changed = True
                    
        I_seq.append(Ik)
        if not Ik or Ik == {0}:
            return True
            
    return False

def conditions(witness):
    """
    witness should be a dictionary representing a finite (possibly non-associative) ring:
    {
        'n': int,                 # number of elements, 0 is the additive identity
        'add': list[list[int]],   # n x n addition table
        'mult': list[list[int]],  # n x n multiplication table
        'I': list[int],           # elements of ideal I
        'J': list[int]            # elements of ideal J
    }
    """
    try:
        n = witness['n']
        add = witness['add']
        mult = witness['mult']
        I = witness['I']
        J = witness['J']
        
        if not check_ring(n, add, mult):
            return [False, False, False]
            
        h1 = is_ideal(n, add, mult, I) and is_nilpotent_ideal(n, add, mult, I)
        h2 = is_ideal(n, add, mult, J) and is_nilpotent_ideal(n, add, mult, J)
        
        IJ = set(I).union(set(J))
        changed = True
        while changed:
            changed = False
            new_elements = list(IJ)
            for x in new_elements:
                for y in new_elements:
                    s = add[x][y]
                    if s not in IJ:
                        IJ.add(s)
                        changed = True
            new_elements = list(IJ)
            for x in new_elements:
                inv_x = next(m for m in range(n) if add[x][m] == 0)
                if inv_x not in IJ:
                    IJ.add(inv_x)
                    changed = True
                    
        is_IJ_ideal = is_ideal(n, add, mult, list(IJ))
        is_IJ_nilpotent = is_nilpotent_ideal(n, add, mult, list(IJ))
        
        neg_q = is_IJ_ideal and not is_IJ_nilpotent
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a nilpotent ideal of R",
    "H_2: J is a nilpotent ideal of R",
    "¬Q: The sum ideal I + J is not a nilpotent ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2