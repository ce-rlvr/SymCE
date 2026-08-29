import itertools
import functools
import math
from sympy import symbols, Rational, Integer

CONDITION_LABELS = [
    "H_1: R and T are commutative rings with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: f: R \\to T is a ring homomorphism",
    "H_4: f(s) is a unit in T for all s \\in S",
    "¬Q: There does not exist a unique ring homomorphism g: S^{-1}R \\to T such that f = g \\circ \\phi"
]

N_HYP = 4
NEG_Q_INDEX = 4

def get_id(size, mul):
    for o in range(size):
        if all(mul[o][a] == a for a in range(size)) and all(mul[a][o] == a for a in range(size)): 
            return o
    return None

def get_zero(size, add):
    for z in range(size):
        if all(add[z][a] == a for a in range(size)) and all(add[a][z] == a for a in range(size)):
            return z
    return None

def is_unit(x, size, mul):
    one = get_id(size, mul)
    if one is None: 
        return False
    for y in range(size):
        if mul[x][y] == one and mul[y][x] == one:
            return True
    return False

def get_inv(size, mul, a):
    one = get_id(size, mul)
    for b in range(size):
        if mul[a][b] == one and mul[b][a] == one:
            return b
    return None

def is_comm_ring_with_id(size, add, mul):
    if size < 1: 
        return False
    for a in range(size):
        for b in range(size):
            if not (0 <= add[a][b] < size): return False
            if not (0 <= mul[a][b] < size): return False
            if add[a][b] != add[b][a]: return False
            if mul[a][b] != mul[b][a]: return False
    for a in range(size):
        for b in range(size):
            for c in range(size):
                if add[a][add[b][c]] != add[add[a][b]][c]: return False
                if mul[a][mul[b][c]] != mul[mul[a][b]][c]: return False
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
    zero = get_zero(size, add)
    if zero is None: 
        return False
    for a in range(size):
        if not any(add[a][b] == zero for b in range(size)): 
            return False
    one = get_id(size, mul)
    if one is None: 
        return False
    return True

def evaluate_neg_Q(R_size, R_add, R_mul, T_size, T_add, T_mul, S, f):
    if not S:
        return True
        
    zero_R = get_zero(R_size, R_add)
    one_R = get_id(R_size, R_mul)
    zero_T = get_zero(T_size, T_add)
    one_T = get_id(T_size, T_mul)
    
    if zero_R is None or one_R is None or zero_T is None or one_T is None:
        return True
        
    def get_neg_R(a):
        for b in range(R_size):
            if R_add[a][b] == zero_R: return b
        return None

    pairs = [(r, s) for r in range(R_size) for s in S]
    classes = []
    for p in pairs:
        found = False
        for c in classes:
            r1, s1 = p
            r2, s2 = c[0]
            term1 = R_mul[r1][s2]
            term2 = R_mul[r2][s1]
            neg_term2 = get_neg_R(term2)
            if neg_term2 is None: return True
            diff = R_add[term1][neg_term2]
            if any(R_mul[u][diff] == zero_R for u in S):
                c.append(p)
                found = True
                break
        if not found:
            classes.append([p])
            
    g_map = {}
    for i, c in enumerate(classes):
        r, s = c[0]
        inv_fs = get_inv(T_size, T_mul, f[s])
        if inv_fs is None: return True
        val = T_mul[f[r]][inv_fs]
        for (r_i, s_i) in c:
            inv_fsi = get_inv(T_size, T_mul, f[s_i])
            if inv_fsi is None or T_mul[f[r_i]][inv_fsi] != val:
                return True
        g_map[i] = val
        
    for i, c1 in enumerate(classes):
        for j, c2 in enumerate(classes):
            r1, s1 = c1[0]
            r2, s2 = c2[0]
            
            r_add = R_add[R_mul[r1][s2]][R_mul[r2][s1]]
            s_add = R_mul[s1][s2]
            if s_add not in S: return True
            
            add_idx = None
            for k, c3 in enumerate(classes):
                r3, s3 = c3[0]
                term1 = R_mul[r_add][s3]
                term2 = R_mul[r3][s_add]
                neg_term2 = get_neg_R(term2)
                if neg_term2 is None: return True
                diff = R_add[term1][neg_term2]
                if any(R_mul[u][diff] == zero_R for u in S):
                    add_idx = k
                    break
            if add_idx is None or g_map[add_idx] != T_add[g_map[i]][g_map[j]]:
                return True
                
            r_mul = R_mul[r1][r2]
            s_mul = R_mul[s1][s2]
            if s_mul not in S: return True
            
            mul_idx = None
            for k, c3 in enumerate(classes):
                r3, s3 = c3[0]
                term1 = R_mul[r_mul][s3]
                term2 = R_mul[r3][s_mul]
                neg_term2 = get_neg_R(term2)
                if neg_term2 is None: return True
                diff = R_add[term1][neg_term2]
                if any(R_mul[u][diff] == zero_R for u in S):
                    mul_idx = k
                    break
            if mul_idx is None or g_map[mul_idx] != T_mul[g_map[i]][g_map[j]]:
                return True
                
    s = S[0]
    one_idx = None
    for k, c3 in enumerate(classes):
        r3, s3 = c3[0]
        term1 = R_mul[s][s3]
        term2 = R_mul[r3][s]
        neg_term2 = get_neg_R(term2)
        if neg_term2 is None: return True
        diff = R_add[term1][neg_term2]
        if any(R_mul[u][diff] == zero_R for u in S):
            one_idx = k
            break
    if one_idx is None or g_map[one_idx] != one_T:
        return True
        
    for r in range(R_size):
        phi_idx = None
        rs = R_mul[r][s]
        for k, c3 in enumerate(classes):
            r3, s3 = c3[0]
            term1 = R_mul[rs][s3]
            term2 = R_mul[r3][s]
            neg_term2 = get_neg_R(term2)
            if neg_term2 is None: return True
            diff = R_add[term1][neg_term2]
            if any(R_mul[u][diff] == zero_R for u in S):
                phi_idx = k
                break
        if phi_idx is None or g_map[phi_idx] != f[r]:
            return True
            
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_size = witness['R_size']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            T_size = witness['T_size']
            T_add = witness['T_add']
            T_mul = witness['T_mul']
            S = witness['S']
            f = witness['f']
        elif isinstance(witness, tuple) and len(witness) == 4:
            n, m, S, f = witness
            R_size = n
            R_add = [[(i + j) % n for j in range(n)] for i in range(n)]
            R_mul = [[(i * j) % n for j in range(n)] for i in range(n)]
            T_size = m
            T_add = [[(i + j) % m for j in range(m)] for i in range(m)]
            T_mul = [[(i * j) % m for j in range(m)] for i in range(m)]
        elif isinstance(witness, tuple) and len(witness) == 8:
            R_size, R_add, R_mul, T_size, T_add, T_mul, S, f = witness
        else:
            R_size = witness.R_size
            R_add = witness.R_add
            R_mul = witness.R_mul
            T_size = witness.T_size
            T_add = witness.T_add
            T_mul = witness.T_mul
            S = witness.S
            f = witness.f

        if callable(f):
            f = [f(i) for i in range(R_size)]
    except Exception:
        return [False] * 5

    # H1: R and T are commutative rings with identity
    try:
        h1 = is_comm_ring_with_id(R_size, R_add, R_mul) and is_comm_ring_with_id(T_size, T_add, T_mul)
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        h2 = all(s in range(R_size) for s in S) and all(R_mul[a][b] in S for a in S for b in S)
    except Exception:
        h2 = False

    # H3: f: R \to T is a ring homomorphism
    try:
        h3 = True
        for a in range(R_size):
            for b in range(R_size):
                if f[R_add[a][b]] != T_add[f[a]][f[b]]: h3 = False
                if f[R_mul[a][b]] != T_mul[f[a]][f[b]]: h3 = False
        
        id_R = get_id(R_size, R_mul)
        id_T = get_id(T_size, T_mul)
        if id_R is not None and id_T is not None:
            if f[id_R] != id_T: 
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: f(s) is a unit in T for all s \in S
    try:
        h4 = all(is_unit(f[s], T_size, T_mul) for s in S)
    except Exception:
        h4 = False

    # neg_Q: The conclusion FAILS
    try:
        neg_Q = evaluate_neg_Q(R_size, R_add, R_mul, T_size, T_add, T_mul, S, f)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]