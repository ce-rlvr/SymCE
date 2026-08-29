import itertools

def make_Zn(n):
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add, mul)

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)
Z7 = make_Zn(7)
Z8 = make_Zn(8)
Z9 = make_Zn(9)
Z10 = make_Zn(10)
Z11 = make_Zn(11)
Z12 = make_Zn(12)

def is_commutative_ring(n, add, mul):
    if n <= 0: return False
    for table in (add, mul):
        if len(table) != n: return False
        for row in table:
            if len(row) != n: return False
            for x in row:
                if not (0 <= x < n): return False
                
    for i in range(n):
        if add[i][0] != i or add[0][i] != i: return False
        
    for i in range(n):
        if not any(add[i][j] == 0 for j in range(n)): return False
        
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    has_id = False
    for e in range(n):
        if all(mul[i][e] == i and mul[e][i] == i for i in range(n)):
            has_id = True
            break
    if not has_id: return False
    
    return True

def ideal_generated_by_fast(n, add, P_ideals, S):
    I = {0}
    for s in S:
        if s == 0: continue
        P = P_ideals[s]
        I = {add[x][y] for x in I for y in P}
    return frozenset(I)

def poly_mul(n, add, mul, f, g):
    if not f or not g: return [0]
    res = [0] * (len(f) + len(g) - 1)
    for i in range(len(f)):
        if f[i] == 0: continue
        for j in range(len(g)):
            if g[j] == 0: continue
            prod = mul[f[i]][g[j]]
            res[i+j] = add[res[i+j]][prod]
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res

def check_Q_fast(n, add, mul, f):
    if len(f) <= 1:
        return True
    
    P_ideals = [{mul[r][s] for r in range(n)} for s in range(n)]
    cf = ideal_generated_by_fast(n, add, P_ideals, f)
    
    for deg_g in range(3):
        for g in itertools.product(range(n), repeat=deg_g + 1):
            g = list(g)
            cg = ideal_generated_by_fast(n, add, P_ideals, g)
            fg = poly_mul(n, add, mul, f, g)
            cfg = ideal_generated_by_fast(n, add, P_ideals, fg)
            
            generators = {mul[x][y] for x in cf for y in cg}
            cf_cg = ideal_generated_by_fast(n, add, P_ideals, generators)
            
            if cfg != cf_cg:
                return False
    return True

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        ring, f = witness
        if not isinstance(ring, (tuple, list)) or len(ring) != 3:
            return [False, False]
        n, add, mul = ring
        
        if isinstance(f, int):
            f = [f]
        f = list(f)
        if not all(isinstance(c, int) and 0 <= c < n for c in f):
            return [False, False]
            
    except Exception:
        return [False, False]
        
    try:
        h1 = is_commutative_ring(n, add, mul)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            P_ideals = [{mul[r][s] for r in range(n)} for s in range(n)]
            cf = ideal_generated_by_fast(n, add, P_ideals, f)
            
            P = (len(cf) == n)
            Q = check_Q_fast(n, add, mul, f)
            
            neg_q = (P != Q)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: R is a commutative ring", "not Q: conclusion fails"]
N_HYP = 1
NEG_Q_INDEX = 1