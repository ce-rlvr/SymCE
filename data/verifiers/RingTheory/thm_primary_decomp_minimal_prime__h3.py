import itertools

# Top-level setup
# The witness is expected to be a dictionary or tuple containing the finite ring's
# size, addition table, multiplication table, and the ideals Q and P.
# Example: witness = {'n': 4, 'add': [...], 'mul': [...], 'Q': [0], 'P': []}

def find_zero(n, add):
    for z in range(n):
        is_zero = True
        for a in range(n):
            if add[a][z] != a or add[z][a] != a:
                is_zero = False
                break
        if is_zero:
            return z
    return None

def is_commutative_ring(n, add, mul):
    if n <= 0: return False
    z = find_zero(n, add)
    if z is None: return False
    
    # Check addition is an abelian group
    for a in range(n):
        for b in range(n):
            if add[a][b] != add[b][a]: return False
            for c in range(n):
                if add[add[a][b]][c] != add[a][add[b][c]]: return False
                
    # Check additive inverses
    for a in range(n):
        has_inv = False
        for b in range(n):
            if add[a][b] == z and add[b][a] == z:
                has_inv = True
                break
        if not has_inv: return False
        
    # Check multiplication is commutative and associative
    for a in range(n):
        for b in range(n):
            if mul[a][b] != mul[b][a]: return False
            for c in range(n):
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return False
                
    # Check distributivity
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
                if mul[add[a][b]][c] != add[mul[a][c]][mul[b][c]]: return False
                
    return True

def is_ideal(S, n, add, mul):
    if not S: return False
    z = find_zero(n, add)
    if z not in S: return False
    
    # Closed under addition
    for x in S:
        for y in S:
            if add[x][y] not in S: return False
            
    # Closed under multiplication by any ring element
    for x in S:
        for r in range(n):
            if mul[x][r] not in S: return False
            if mul[r][x] not in S: return False
            
    # Closed under additive inverse
    for x in S:
        inv_x = None
        for y in range(n):
            if add[x][y] == z and add[y][x] == z:
                inv_x = y
                break
        if inv_x not in S: return False
        
    return True

def is_primary(Q, n, add, mul):
    if not is_ideal(Q, n, add, mul): return False
    if set(Q) == set(range(n)): return False # Must be a proper ideal
    
    for a in range(n):
        for b in range(n):
            if mul[a][b] in Q:
                if a in Q: continue
                # Check if b^k is in Q for some k > 0
                b_k = b
                found = False
                for k in range(1, n + 1):
                    if b_k in Q:
                        found = True
                        break
                    b_k = mul[b_k][b]
                if not found:
                    return False
    return True

def is_prime(P, n, add, mul):
    if not is_ideal(P, n, add, mul): return False
    if set(P) == set(range(n)): return False # Must be a proper ideal
    
    for a in range(n):
        for b in range(n):
            if mul[a][b] in P:
                if a not in P and b not in P:
                    return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            Q = list(witness['Q'])
            P = list(witness['P'])
        else:
            n, add, mul, Q, P = witness
            Q = list(Q)
            P = list(P)
            
        # Limit size to prevent timeout
        if n > 12:
            return [False, False, False]
            
        h1 = is_commutative_ring(n, add, mul)
        h2 = is_primary(Q, n, add, mul)
        
        # Find all prime ideals containing Q
        primes_containing_Q = []
        for i in range(1 << n):
            subset = [x for x in range(n) if (i & (1 << x))]
            if set(Q).issubset(set(subset)):
                if is_prime(subset, n, add, mul):
                    primes_containing_Q.append(set(subset))
                    
        # Filter to find the minimal prime ideals containing Q
        minimal_primes = []
        for p1 in primes_containing_Q:
            is_minimal = True
            for p2 in primes_containing_Q:
                if p2 < p1: # p2 is a proper subset of p1
                    is_minimal = False
                    break
            if is_minimal:
                minimal_primes.append(p1)
                
        # The conclusion states that P is the unique minimal prime ideal containing Q
        conclusion_holds = (len(minimal_primes) == 1) and (set(P) == minimal_primes[0])
        neg_q = not conclusion_holds
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a primary ideal of R",
    "¬Q: P is not the unique minimal prime ideal containing Q"
]

N_HYP = 2
NEG_Q_INDEX = 2