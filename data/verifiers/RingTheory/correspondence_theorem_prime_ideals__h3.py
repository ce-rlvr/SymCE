import itertools

# Expected witness format:
# witness = (n, add_table, mul_table, I_set)
# where:
#   n: int, size of the ring
#   add_table: list[list[int]], n x n addition table
#   mul_table: list[list[int]], n x n multiplication table
#   I_set: list[int], elements of the ideal I

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: The mapping P \\mapsto \\pi(P) is NOT a bijection between prime ideals of R containing I and prime ideals of R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_tables(n, add, mul):
    if not isinstance(n, int) or n <= 0: return False
    if not isinstance(add, list) or not isinstance(mul, list): return False
    if len(add) != n or len(mul) != n: return False
    for i in range(n):
        if not isinstance(add[i], list) or not isinstance(mul[i], list): return False
        if len(add[i]) != n or len(mul[i]) != n: return False
        for j in range(n):
            if not isinstance(add[i][j], int) or not isinstance(mul[i][j], int): return False
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
    return True

def is_commutative_ring_with_identity(n, add, mul):
    if n <= 0: return False
    # Check addition
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
    
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
        
    # Check multiplication
    for i in range(n):
        for j in range(n):
            if mul[i][j] != mul[j][i]: return False
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    identity = -1
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)):
            identity = i
            break
    if identity == -1: return False
    
    # Check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    return True

def is_ideal(n, add, mul, I_set):
    if not isinstance(I_set, (list, set, frozenset)): return False
    if not I_set: return False
    I_set = set(I_set)
    if not all(isinstance(x, int) and 0 <= x < n for x in I_set): return False
    
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero not in I_set: return False
    
    for a in I_set:
        for b in I_set:
            if add[a][b] not in I_set: return False
            
    for a in I_set:
        inv_found = False
        for b in I_set:
            if add[a][b] == zero:
                inv_found = True
                break
        if not inv_found: return False
        
    for a in I_set:
        for r in range(n):
            if mul[a][r] not in I_set: return False
            if mul[r][a] not in I_set: return False
            
    return True

def is_prime_ideal(n, add, mul, P_set):
    if not is_ideal(n, add, mul, P_set): return False
    if len(P_set) == n: return False
    
    for a in range(n):
        for b in range(n):
            if mul[a][b] in P_set:
                if a not in P_set and b not in P_set:
                    return False
    return True

def get_all_ideals(n, add, mul):
    principal_ideals = set()
    for i in range(n):
        P = set()
        for r in range(n):
            P.add(mul[r][i])
        principal_ideals.add(frozenset(P))
        
    ideals = set(principal_ideals)
    queue = list(principal_ideals)
    
    while queue:
        I1 = queue.pop(0)
        for I2 in principal_ideals:
            S = set()
            for a in I1:
                for b in I2:
                    S.add(add[a][b])
            I3 = frozenset(S)
            if I3 not in ideals:
                ideals.add(I3)
                queue.append(I3)
                
    return ideals

def get_prime_ideals(n, add, mul):
    ideals = get_all_ideals(n, add, mul)
    prime_ideals = []
    for I in ideals:
        if is_prime_ideal(n, add, mul, I):
            prime_ideals.append(I)
    return prime_ideals

def get_cosets(n, add, I_set):
    cosets = set()
    for r in range(n):
        coset = frozenset(add[r][i] for i in I_set)
        cosets.add(coset)
    return list(cosets)

def build_quotient_ring(n, add, mul, I_set):
    cosets = get_cosets(n, add, I_set)
    m = len(cosets)
    coset_to_idx = {c: i for i, c in enumerate(cosets)}
    
    q_add = [[0]*m for _ in range(m)]
    q_mul = [[0]*m for _ in range(m)]
    
    for i, c1 in enumerate(cosets):
        for j, c2 in enumerate(cosets):
            r1 = next(iter(c1))
            r2 = next(iter(c2))
            
            sum_r = add[r1][r2]
            prod_r = mul[r1][r2]
            
            sum_c = frozenset(add[sum_r][x] for x in I_set)
            prod_c = frozenset(add[prod_r][x] for x in I_set)
            
            if sum_c not in coset_to_idx or prod_c not in coset_to_idx:
                raise ValueError("Not a valid quotient ring")
                
            q_add[i][j] = coset_to_idx[sum_c]
            q_mul[i][j] = coset_to_idx[prod_c]
            
    return m, q_add, q_mul, cosets, coset_to_idx

def check_conclusion(n, add, mul, I_set):
    prime_ideals_R = get_prime_ideals(n, add, mul)
    
    I_frozenset = frozenset(I_set)
    primes_containing_I = [P for P in prime_ideals_R if I_frozenset.issubset(P)]
    
    m, q_add, q_mul, cosets, coset_to_idx = build_quotient_ring(n, add, mul, I_set)
    
    prime_ideals_q = get_prime_ideals(m, q_add, q_mul)
    
    mapped_primes = []
    for P in primes_containing_I:
        pi_P = set()
        for p in P:
            coset = frozenset(add[p][x] for x in I_set)
            pi_P.add(coset_to_idx[coset])
        mapped_primes.append(frozenset(pi_P))
        
    if len(mapped_primes) != len(set(mapped_primes)):
        return False
        
    set_mapped = set(mapped_primes)
    set_q_primes = set(prime_ideals_q)
    
    if set_mapped != set_q_primes:
        return False
        
    return True

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 4:
            return [False, False, False]
        n, add, mul, I_set = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_tables(n, add, mul) and is_commutative_ring_with_identity(n, add, mul)
    except Exception:
        h1 = False
        
    try:
        h2 = check_tables(n, add, mul) and is_ideal(n, add, mul, I_set) and len(I_set) < n
    except Exception:
        h2 = False
        
    try:
        if not (check_tables(n, add, mul) and is_commutative_ring_with_identity(n, add, mul) and is_ideal(n, add, mul, I_set)):
            neg_q = False
        else:
            q_holds = check_conclusion(n, add, mul, I_set)
            neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]