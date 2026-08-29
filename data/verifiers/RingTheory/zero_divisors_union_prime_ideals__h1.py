import itertools

# Top-level setup: named object bindings that the witness expression may reference.
def _build_Zn(n):
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mult = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add, mult)

Z2 = _build_Zn(2)
Z3 = _build_Zn(3)
Z4 = _build_Zn(4)
Z6 = _build_Zn(6)
Z8 = _build_Zn(8)

def _build_M2_Z2():
    # 2x2 matrices over Z2
    matrices = list(itertools.product([0, 1], repeat=4))
    n = 16
    add = [[0]*n for _ in range(n)]
    mult = [[0]*n for _ in range(n)]
    for i, A in enumerate(matrices):
        for j, B in enumerate(matrices):
            s0 = (A[0] + B[0]) % 2
            s1 = (A[1] + B[1]) % 2
            s2 = (A[2] + B[2]) % 2
            s3 = (A[3] + B[3]) % 2
            s = (s0, s1, s2, s3)
            add[i][j] = matrices.index(s)
            
            p0 = (A[0]*B[0] + A[1]*B[2]) % 2
            p1 = (A[0]*B[1] + A[1]*B[3]) % 2
            p2 = (A[2]*B[0] + A[3]*B[2]) % 2
            p3 = (A[2]*B[1] + A[3]*B[3]) % 2
            p = (p0, p1, p2, p3)
            mult[i][j] = matrices.index(p)
    return (n, add, mult)

M2_Z2 = _build_M2_Z2()

def _build_UT2_Z2():
    # Upper triangular 2x2 matrices over Z2
    matrices = list(itertools.product([0, 1], repeat=3))
    n = 8
    add = [[0]*n for _ in range(n)]
    mult = [[0]*n for _ in range(n)]
    for i, A in enumerate(matrices):
        for j, B in enumerate(matrices):
            s0 = (A[0] + B[0]) % 2
            s1 = (A[1] + B[1]) % 2
            s2 = (A[2] + B[2]) % 2
            s = (s0, s1, s2)
            add[i][j] = matrices.index(s)
            
            p0 = (A[0]*B[0]) % 2
            p1 = (A[0]*B[1] + A[1]*B[2]) % 2
            p2 = (A[2]*B[2]) % 2
            p = (p0, p1, p2)
            mult[i][j] = matrices.index(p)
    return (n, add, mult)

UT2_Z2 = _build_UT2_Z2()

CONDITION_LABELS = [
    "H_1: S is the set of all zero divisors of R",
    "¬Q: S is not a union of prime ideals of R"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple (n, add_table, mult_table)
        if not (isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int)):
            return [False, False]
            
        n, add, mult = witness
        
        if n <= 0:
            return [False, False]
            
        # Check if R is a valid ring
        is_ring = True
        # check add commutative
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: is_ring = False
        # check add associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: is_ring = False
        # check add identity (0)
        for i in range(n):
            if add[i][0] != i or add[0][i] != i: is_ring = False
        # check add inverse
        for i in range(n):
            has_inv = False
            for j in range(n):
                if add[i][j] == 0:
                    has_inv = True
                    break
            if not has_inv: is_ring = False
        # check mult associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mult[mult[i][j]][k] != mult[i][mult[j][k]]: is_ring = False
        # check distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mult[i][add[j][k]] != add[mult[i][j]][mult[i][k]]: is_ring = False
                    if mult[add[i][j]][k] != add[mult[i][k]][mult[j][k]]: is_ring = False
                    
        # check multiplicative identity
        has_id = False
        for i in range(n):
            is_id = True
            for j in range(n):
                if mult[i][j] != j or mult[j][i] != j:
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
                
        h1 = is_ring and has_id
        if not h1:
            return [False, False]
            
        # Compute S (the set of all zero divisors of R)
        S = set()
        for a in range(n):
            for b in range(n):
                if b != 0:
                    if mult[a][b] == 0 or mult[b][a] == 0:
                        S.add(a)
                        break
                        
        # Compute all ideals of R
        def closure(subset):
            s = set(subset)
            while True:
                size = len(s)
                new_s = set(s)
                for x in s:
                    for y in s:
                        new_s.add(add[x][y])
                    for r in range(n):
                        new_s.add(mult[x][r])
                        new_s.add(mult[r][x])
                s = new_s
                if len(s) == size:
                    break
            return frozenset(s)
            
        principal_ideals = set()
        for i in range(n):
            principal_ideals.add(closure([i]))
            
        ideals = set(principal_ideals)
        while True:
            size = len(ideals)
            new_ideals = set(ideals)
            for I1 in ideals:
                for I2 in principal_ideals:
                    new_ideals.add(closure(I1 | I2))
            ideals = new_ideals
            if len(ideals) == size:
                break
                
        def ideal_product(A, B):
            prods = set()
            for a in A:
                for b in B:
                    prods.add(mult[a][b])
            return closure(prods)
            
        # Find all prime ideals
        prime_ideals = []
        for P in ideals:
            if len(P) == n:
                continue  # Prime ideals must be proper
            is_prime = True
            for A in ideals:
                for B in ideals:
                    prod = ideal_product(A, B)
                    if prod.issubset(P):
                        if not (A.issubset(P) or B.issubset(P)):
                            is_prime = False
                            break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(P)
                
        # Check if S is a union of prime ideals
        union_of_primes = set()
        for P in prime_ideals:
            if P.issubset(S):
                union_of_primes.update(P)
                
        neg_q = (union_of_primes != S)
        
        return [True, neg_q]
        
    except Exception:
        return [False, False]