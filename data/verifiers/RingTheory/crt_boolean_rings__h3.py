import itertools

def make_boolean_ring(k):
    n = 2**k
    add_table = [[i ^ j for j in range(n)] for i in range(n)]
    mul_table = [[i & j for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

B1 = make_boolean_ring(1)
B2 = make_boolean_ring(2)
B3 = make_boolean_ring(3)
B4 = make_boolean_ring(4)

def is_boolean_ring(n, add, mul):
    if not isinstance(n, int) or n < 1 or n > 256: 
        return False
    if len(add) != n or len(mul) != n: 
        return False
    for i in range(n):
        if len(add[i]) != n or len(mul[i]) != n: 
            return False
        for j in range(n):
            if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n): 
                return False
            if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < n): 
                return False
            
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: 
                return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: 
                    return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: 
                    return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: 
                    return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: 
                    return False
                
    has_zero = False
    for z in range(n):
        if all(add[z][i] == i for i in range(n)):
            has_zero = True
            zero = z
            break
    if not has_zero: 
        return False
    
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): 
            return False
        
    for i in range(n):
        if mul[i][i] != i: 
            return False
        
    return True

def conditions(witness):
    try:
        ring, x, y = witness
        n, add, mul = ring
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_boolean_ring(n, add, mul)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(h1 and isinstance(x, int) and isinstance(y, int) and 0 <= x < n and 0 <= y < n)
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            ideal_x = set(mul[r][x] for r in range(n))
            ideal_y = set(mul[s][y] for s in range(n))
            sum_ideal = set()
            for a in ideal_x:
                for b in ideal_y:
                    sum_ideal.add(add[a][b])
            neg_q = bool(len(sum_ideal) < n)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x and y are elements of R",
    "¬Q: The principal ideals (x) and (y) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2