import itertools

# Top-level setup
# The witness is expected to be a tuple: (n, add_table, mul_table, I, J)
# where n is the size of the ring, add_table and mul_table are n x n lists
# representing the addition and multiplication tables, and I, J are lists/sets 
# of integers in range(n) representing the subsets.

def is_commutative_ring(n, add_table, mul_table):
    if n <= 0: return False
    for i in range(n):
        for j in range(n):
            if not (0 <= add_table[i][j] < n): return False
            if not (0 <= mul_table[i][j] < n): return False
            
    # Additive identity (0)
    for i in range(n):
        if add_table[i][0] != i or add_table[0][i] != i:
            return False
            
    # Additive inverse
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add_table[i][j] == 0 and add_table[j][i] == 0:
                has_inv = True
                break
        if not has_inv: return False
        
    # Commutativity of add
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            
    # Associativity of add
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                    return False
                    
    # Commutativity of mul
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]: return False
            
    # Associativity of mul
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                    return False
                    
    # Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                    return False
                    
    return True

def is_ideal(I, n, add_table, mul_table):
    if not I: return False
    I_set = set(I)
    if not I_set.issubset(range(n)): return False
    if 0 not in I_set: return False
    
    for a in I_set:
        for b in I_set:
            if add_table[a][b] not in I_set: return False
            
    for r in range(n):
        for a in I_set:
            if mul_table[r][a] not in I_set: return False
            
    return True

def subset_mul(A, B, n, add_table, mul_table):
    closure = {mul_table[a][b] for a in A for b in B}
    if not closure:
        return closure
    
    queue = list(closure)
    head = 0
    while head < len(queue):
        x = queue[head]
        head += 1
        for i in range(len(queue)):
            y = queue[i]
            s = add_table[x][y]
            if s not in closure:
                closure.add(s)
                queue.append(s)
    return closure

def integral_closure_subset(A, n, add_table, mul_table):
    closure = set()
    for x in range(n):
        S = set(A)
        A_pow = set(A)
        x_pow = x
        
        is_in_closure = False
        for k in range(1, n + 1):
            if x_pow in S:
                is_in_closure = True
                break
            if k < n:
                x_pow = mul_table[x_pow][x]
                A_pow = subset_mul(A_pow, A, n, add_table, mul_table)
                xS = {mul_table[x][s] for s in S}
                S = {add_table[a][b] for a in xS for b in A_pow}
                
        if is_in_closure:
            closure.add(x)
            
    return closure

def conditions(witness):
    try:
        n, add_table, mul_table, I, J = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(I, n, add_table, mul_table)
    except Exception:
        h2 = False
        
    try:
        I_bar = integral_closure_subset(I, n, add_table, mul_table)
        J_bar = integral_closure_subset(J, n, add_table, mul_table)
        
        IJ = subset_mul(I, J, n, add_table, mul_table)
        IJ_bar = integral_closure_subset(IJ, n, add_table, mul_table)
        
        I_bar_J_bar = subset_mul(I_bar, J_bar, n, add_table, mul_table)
        
        q = I_bar_J_bar.issubset(IJ_bar)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: \\overline{I} \\cdot \\overline{J} \\not\\subseteq \\overline{IJ}"
]

N_HYP = 2
NEG_Q_INDEX = 2