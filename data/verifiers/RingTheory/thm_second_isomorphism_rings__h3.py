import sympy
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring(R):
    if not R: 
        return False
    for a in R:
        for b in R:
            if (a - b) not in R: 
                return False
            if (a * b) not in R: 
                return False
    return True

def is_subring(S, R):
    if not S: 
        return False
    if not all(x in R for x in S): 
        return False
    return is_ring(S)

def is_ideal(I, R):
    if not is_subring(I, R): 
        return False
    for r in R:
        for i in I:
            if (r * i) not in I: 
                return False
            if (i * r) not in I: 
                return False
    return True

def set_add(S, I):
    res = []
    for s in S:
        for i in I:
            val = s + i
            if val not in res:
                res.append(val)
    return res

def set_intersect(S, I):
    res = []
    for s in S:
        if s in I and s not in res:
            res.append(s)
    return res

def build_quotient_table(A, J):
    reps = []
    for a in A:
        if not any((a - r) in J for r in reps):
            reps.append(a)
    
    n = len(reps)
    add_table = [[0] * n for _ in range(n)]
    mul_table = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            sum_val = reps[i] + reps[j]
            for k in range(n):
                if (sum_val - reps[k]) in J:
                    add_table[i][j] = k
                    break
            else:
                raise ValueError("Not closed under addition modulo J")
            
            mul_val = reps[i] * reps[j]
            for k in range(n):
                if (mul_val - reps[k]) in J:
                    mul_table[i][j] = k
                    break
            else:
                raise ValueError("Not closed under multiplication modulo J")
                
    return add_table, mul_table

def are_isomorphic(table1, table2):
    add1, mul1 = table1
    add2, mul2 = table2
    n = len(add1)
    if len(add2) != n: 
        return False
    if n == 0: 
        return True

    def find_zero(add):
        for i in range(n):
            if add[i][i] == i:
                return i
        return None
    
    z1 = find_zero(add1)
    z2 = find_zero(add2)
    if z1 is None or z2 is None: 
        return False

    mapping = {}
    used = set()

    def solve(i):
        if i == n:
            return True
        if i in mapping:
            return solve(i + 1)
            
        for j in range(n):
            if j in used: 
                continue
            
            mapping[i] = j
            
            consistent = True
            for x in mapping:
                for y in mapping:
                    res_add = add1[x][y]
                    if res_add in mapping and mapping[res_add] != add2[mapping[x]][mapping[y]]:
                        consistent = False
                        break
                    
                    res_mul = mul1[x][y]
                    if res_mul in mapping and mapping[res_mul] != mul2[mapping[x]][mapping[y]]:
                        consistent = False
                        break
                if not consistent: 
                    break
            
            if consistent:
                used.add(j)
                if solve(i + 1):
                    return True
                used.remove(j)
                
            del mapping[i]
            
        return False

    mapping[z1] = z2
    used.add(z2)
    return solve(0)

def check_Q(R, S, I):
    S_int_I = set_intersect(S, I)
    if not is_ideal(S_int_I, S): 
        return False
    
    S_plus_I = set_add(S, I)
    if not is_subring(S_plus_I, R): 
        return False
    
    if not is_ideal(I, S_plus_I): 
        return False
    
    try:
        table1 = build_quotient_table(S_plus_I, I)
        table2 = build_quotient_table(S, S_int_I)
    except ValueError:
        return False
    
    if not are_isomorphic(table1, table2): 
        return False
    
    return True

def conditions(witness):
    try:
        R, S, I = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subring(S, R)
    except Exception:
        h2 = False
        
    try:
        q = check_Q(R, S, I)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: S is a subring of R",
    "¬Q: The conclusion fails (S \\cap I is not an ideal of S, or S+I is not a subring of R, or (S+I)/I is not isomorphic to S/(S \\cap I))"
]

N_HYP = 2
NEG_Q_INDEX = 2