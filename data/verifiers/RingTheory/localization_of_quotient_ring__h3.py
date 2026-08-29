import itertools

# Top-level setup: named object bindings that the witness expression may reference.
def _make_Zn(n):
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return n, add_table, mul_table

def _make_product_ring(ring1, ring2):
    n1, add1, mul1 = ring1
    n2, add2, mul2 = ring2
    N = n1 * n2
    add_table = [[0]*N for _ in range(N)]
    mul_table = [[0]*N for _ in range(N)]
    
    def encode(i, j): return i * n2 + j
    def decode(x): return x // n2, x % n2
    
    for x in range(N):
        for y in range(N):
            i1, j1 = decode(x)
            i2, j2 = decode(y)
            add_table[x][y] = encode(add1[i1][i2], add2[j1][j2])
            mul_table[x][y] = encode(mul1[i1][i2], mul2[j1][j2])
            
    return N, add_table, mul_table

Z2 = _make_Zn(2)
Z3 = _make_Zn(3)
Z4 = _make_Zn(4)
Z6 = _make_Zn(6)
Z2xZ2 = _make_product_ring(Z2, Z2)

def parse_witness(witness):
    if isinstance(witness, dict):
        N = witness.get('N')
        add_table = witness.get('add_table')
        mul_table = witness.get('mul_table')
        I = witness.get('I')
        S = witness.get('S')
        S_prime = witness.get('S_prime')
    else:
        N = witness[0]
        add_table = witness[1]
        mul_table = witness[2]
        I = witness[3]
        S = witness[4]
        S_prime = witness[5] if len(witness) > 5 else None
    return N, add_table, mul_table, I, S, S_prime

def check_H1(N, add_table, mul_table):
    try:
        if not isinstance(N, int) or N <= 0 or N > 50: return False
        if len(add_table) != N or len(mul_table) != N: return False
        for row in add_table:
            if len(row) != N: return False
        for row in mul_table:
            if len(row) != N: return False
            
        for i in range(N):
            for j in range(N):
                if not (0 <= add_table[i][j] < N): return False
                if not (0 <= mul_table[i][j] < N): return False
                
        for i in range(N):
            for j in range(N):
                if add_table[i][j] != add_table[j][i]: return False
                
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                    
        zero = None
        for i in range(N):
            if all(add_table[i][j] == j for j in range(N)):
                zero = i
                break
        if zero is None: return False
        
        for i in range(N):
            if not any(add_table[i][j] == zero for j in range(N)): return False
            
        for i in range(N):
            for j in range(N):
                if mul_table[i][j] != mul_table[j][i]: return False
                
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    
        one = None
        for i in range(N):
            if all(mul_table[i][j] == j for j in range(N)):
                one = i
                break
        if one is None: return False
        
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    
        return True
    except Exception:
        return False

def check_H2(N, mul_table, S):
    try:
        if not isinstance(S, (list, set, tuple)): return False
        if not S: return False
        for x in S:
            if not (0 <= x < N): return False
            for y in S:
                if mul_table[x][y] not in S: return False
        return True
    except Exception:
        return False

def check_H3(N, add_table, I, S, S_prime):
    try:
        if not isinstance(I, (list, set, tuple)): return False
        if not I: return False
        for x in I:
            if not (0 <= x < N): return False
            
        zero = None
        for i in range(N):
            if all(add_table[i][j] == j for j in range(N)):
                zero = i
                break
        if zero not in I: return False
        
        for x in I:
            for y in I:
                neg_y = None
                for j in range(N):
                    if add_table[y][j] == zero:
                        neg_y = j
                        break
                if add_table[x][neg_y] not in I: return False
                
        if S_prime is None:
            return True
            
        expected_S_prime = set()
        for s in S:
            coset = frozenset(add_table[s][i] for i in I)
            expected_S_prime.add(coset)
            
        actual_S_prime = set()
        for c in S_prime:
            actual_S_prime.add(frozenset(c))
            
        return actual_S_prime == expected_S_prime
    except Exception:
        return False

def is_ideal(M, add_table, mul_table, subset):
    if not subset: return False
    zero = None
    for i in range(M):
        if all(add_table[i][j] == j for j in range(M)):
            zero = i
            break
    if zero not in subset: return False
    
    for x in subset:
        for y in subset:
            neg_y = None
            for j in range(M):
                if add_table[y][j] == zero:
                    neg_y = j
                    break
            if add_table[x][neg_y] not in subset: return False
            
    for x in subset:
        for r in range(M):
            if mul_table[x][r] not in subset: return False
            if mul_table[r][x] not in subset: return False
            
    return True

def get_localization(N, add_table, mul_table, S):
    pairs = [(r, s) for r in range(N) for s in S]
    
    zero = None
    for i in range(N):
        if all(add_table[i][j] == j for j in range(N)):
            zero = i
            break

    def sub(x, y):
        neg_y = None
        for j in range(N):
            if add_table[y][j] == zero:
                neg_y = j
                break
        return add_table[x][neg_y]

    def equiv(p1, p2):
        r1, s1 = p1
        r2, s2 = p2
        term1 = mul_table[r1][s2]
        term2 = mul_table[r2][s1]
        diff = sub(term1, term2)
        for u in S:
            if mul_table[u][diff] == zero:
                return True
        return False

    classes = []
    for p in pairs:
        found = False
        for c in classes:
            if equiv(p, next(iter(c))):
                c.add(p)
                found = True
                break
        if not found:
            classes.append({p})
            
    return [frozenset(c) for c in classes]

def construct_localization(N, add_table, mul_table, S):
    classes = get_localization(N, add_table, mul_table, S)
    
    pair_to_class = {}
    for idx, c in enumerate(classes):
        for p in c:
            pair_to_class[p] = idx
            
    M = len(classes)
    loc_add = [[0]*M for _ in range(M)]
    loc_mul = [[0]*M for _ in range(M)]
    
    for i in range(M):
        for j in range(M):
            r1, s1 = next(iter(classes[i]))
            r2, s2 = next(iter(classes[j]))
            
            term1 = mul_table[r1][s2]
            term2 = mul_table[r2][s1]
            num_add = add_table[term1][term2]
            den_add = mul_table[s1][s2]
            
            if (num_add, den_add) not in pair_to_class: return None
            loc_add[i][j] = pair_to_class[(num_add, den_add)]
            
            num_mul = mul_table[r1][r2]
            den_mul = mul_table[s1][s2]
            
            if (num_mul, den_mul) not in pair_to_class: return None
            loc_mul[i][j] = pair_to_class[(num_mul, den_mul)]
            
    return M, loc_add, loc_mul, classes, pair_to_class

def construct_quotient_ring(N, add_table, mul_table, I):
    if not is_ideal(N, add_table, mul_table, I):
        return None
        
    classes = []
    for x in range(N):
        c = frozenset(add_table[x][i] for i in I)
        if c not in classes:
            classes.append(c)
            
    M = len(classes)
    q_add = [[0]*M for _ in range(M)]
    q_mul = [[0]*M for _ in range(M)]
    
    class_to_idx = {c: i for i, c in enumerate(classes)}
    
    for i in range(M):
        for j in range(M):
            x = next(iter(classes[i]))
            y = next(iter(classes[j]))
            
            sum_xy = add_table[x][y]
            c_sum = frozenset(add_table[sum_xy][k] for k in I)
            q_add[i][j] = class_to_idx[c_sum]
            
            prod_xy = mul_table[x][y]
            c_prod = frozenset(add_table[prod_xy][k] for k in I)
            q_mul[i][j] = class_to_idx[c_prod]
            
    return M, q_add, q_mul, classes

def get_S_inv_I(classes, I, S, pair_to_class):
    subset_indices = set()
    for i in I:
        for s in S:
            if (i, s) in pair_to_class:
                subset_indices.add(pair_to_class[(i, s)])
    return list(subset_indices)

def construct_LHS(N, add_table, mul_table, I, S):
    loc_res = construct_localization(N, add_table, mul_table, S)
    if loc_res is None: return None
    M, loc_add, loc_mul, classes, pair_to_class = loc_res
    
    S_inv_I = get_S_inv_I(classes, I, S, pair_to_class)
    
    return construct_quotient_ring(M, loc_add, loc_mul, S_inv_I)

def construct_RHS(N, add_table, mul_table, I, S):
    q_res = construct_quotient_ring(N, add_table, mul_table, I)
    if q_res is None: return None
    M, q_add, q_mul, classes = q_res
    
    S_prime_indices = set()
    for s in S:
        for idx, c in enumerate(classes):
            if s in c:
                S_prime_indices.add(idx)
                break
    S_prime_indices = list(S_prime_indices)
    
    return construct_localization(M, q_add, q_mul, S_prime_indices)

def extract_ring(ring_res):
    if ring_res is None: return None
    return ring_res[0], ring_res[1], ring_res[2]

def are_isomorphic(ring1, ring2):
    M1, add1, mul1 = ring1
    M2, add2, mul2 = ring2
    
    if M1 != M2:
        return False
        
    for p in itertools.permutations(range(M1)):
        is_iso = True
        for i in range(M1):
            for j in range(M1):
                if p[add1[i][j]] != add2[p[i]][p[j]]:
                    is_iso = False
                    break
                if p[mul1[i][j]] != mul2[p[i]][p[j]]:
                    is_iso = False
                    break
            if not is_iso:
                break
        if is_iso:
            return True
            
    return False

def check_neg_Q(N, add_table, mul_table, I, S):
    try:
        lhs = construct_LHS(N, add_table, mul_table, I, S)
        rhs = construct_RHS(N, add_table, mul_table, I, S)
        
        ring1 = extract_ring(lhs)
        ring2 = extract_ring(rhs)
        
        if ring1 is None or ring2 is None:
            return True
            
        return not are_isomorphic(ring1, ring2)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        N, add_table, mul_table, I, S, S_prime = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    h1 = check_H1(N, add_table, mul_table)
    h2 = check_H2(N, mul_table, S)
    h3 = check_H3(N, add_table, I, S, S_prime)
    
    neg_q = check_neg_Q(N, add_table, mul_table, I, S)
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: S' is the image of S under the canonical projection from R to R/I",
    "¬Q: The localized quotient ring (S^{-1}R)/(S^{-1}I) is NOT isomorphic to (S')^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3