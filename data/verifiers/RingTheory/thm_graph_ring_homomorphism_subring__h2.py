import itertools

# Top-level setup
# Finite rings will be represented by their addition and multiplication tables.
# The witness is expected to be a tuple: (R_add, R_mul, S_add, S_mul, f)
# where R_add, R_mul are n x n lists of lists of ints (0 to n-1),
# S_add, S_mul are m x m lists of lists of ints (0 to m-1),
# and f is a list, dict, or callable mapping 0..n-1 to 0..m-1.

def is_ring(add, mul):
    n = len(add)
    if n == 0: 
        return False
    if len(mul) != n: 
        return False
    for row in add + mul:
        if len(row) != n: 
            return False
        for x in row:
            if not (isinstance(x, int) and 0 <= x < n): 
                return False
            
    # Addition is commutative
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: 
                return False
            
    # Addition is associative
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: 
                    return False
                
    # Additive identity is 0
    for i in range(n):
        if add[0][i] != i or add[i][0] != i: 
            return False
        
    # Additive inverses exist
    for i in range(n):
        if not any(add[i][j] == 0 for j in range(n)): 
            return False
        
    # Multiplication is associative
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: 
                    return False
                
    # Distributive laws
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: 
                    return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: 
                    return False
                
    return True

def conditions(witness):
    try:
        R_add, R_mul, S_add, S_mul, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are rings
    try:
        h1 = is_ring(R_add, R_mul) and is_ring(S_add, S_mul)
    except Exception:
        h1 = False
        
    # H_2: G is the graph of f
    try:
        n = len(R_add)
        m = len(S_add)
        if callable(f):
            f_eval = f
        else:
            f_eval = lambda x: f[x]
            
        f_vals = [f_eval(i) for i in range(n)]
        h2 = all(isinstance(x, int) and 0 <= x < m for x in f_vals)
    except Exception:
        h2 = False
        
    # ¬Q: G is not a subring of R x S
    try:
        is_subring = True
        n = len(R_add)
        
        if callable(f):
            f_eval = f
        else:
            f_eval = lambda x: f[x]
            
        # For G to be a subring, it must contain the additive identity (0, 0)
        if f_eval(0) != 0:
            is_subring = False
            
        # G must be closed under addition and multiplication
        for a in range(n):
            for b in range(n):
                if f_eval(R_add[a][b]) != S_add[f_eval(a)][f_eval(b)]:
                    is_subring = False
                if f_eval(R_mul[a][b]) != S_mul[f_eval(a)][f_eval(b)]:
                    is_subring = False
                    
        neg_q = not is_subring
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: G is the graph of f",
    "¬Q: G is not a subring of R x S"
]

N_HYP = 2
NEG_Q_INDEX = 2