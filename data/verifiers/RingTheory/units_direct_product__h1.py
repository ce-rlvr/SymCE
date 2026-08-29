import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We represent a finite ring as a tuple (n, add_table, mul_table).
def Z(n):
    """Returns the ring Z/nZ."""
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add, mul)

def mZ_n(m, n):
    """Returns the ring mZ/nZ, where m divides n."""
    k = n // m
    add = [[(i + j) % k for j in range(k)] for i in range(k)]
    mul = [[(i * j * m) % k for j in range(k)] for i in range(k)]
    return (k, add, mul)

Z2 = Z(2)
Z3 = Z(3)
Z4 = Z(4)
Z6 = Z(6)

def is_ring(R):
    try:
        if not isinstance(R, tuple) or len(R) != 3: return False
        n, add, mul = R
        if not isinstance(n, int) or n <= 0: return False
        if not isinstance(add, list) or not isinstance(mul, list): return False
        if len(add) != n or len(mul) != n: return False
        for row in add:
            if not isinstance(row, list) or len(row) != n: return False
        for row in mul:
            if not isinstance(row, list) or len(row) != n: return False
            
        # check addition commutative
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
                
        # check addition associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[i][add[j][k]] != add[add[i][j]][k]: return False
                    
        # check addition identity
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        
        # check addition inverse
        for i in range(n):
            if not any(add[i][j] == zero for j in range(n)): return False
            
        # check multiplication associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[i][mul[j][k]] != mul[mul[i][j]][k]: return False
                    
        # check distributive
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                    
        return True
    except Exception:
        return False

def get_identity(R):
    try:
        n, add, mul = R
        for e in range(n):
            if all(mul[e][x] == x for x in range(n)) and all(mul[x][e] == x for x in range(n)):
                return e
        return None
    except Exception:
        return None

def get_unit_group(R):
    try:
        e = get_identity(R)
        if e is None:
            return None
        n, add, mul = R
        units = []
        for x in range(n):
            has_inv = False
            for y in range(n):
                if mul[x][y] == e and mul[y][x] == e:
                    has_inv = True
                    break
            if has_inv:
                units.append(x)
        
        k = len(units)
        table = [[0]*k for _ in range(k)]
        for i in range(k):
            for j in range(k):
                prod = mul[units[i]][units[j]]
                if prod in units:
                    table[i][j] = units.index(prod)
                else:
                    return None
        return table
    except Exception:
        return None

def direct_product_ring(R1, R2):
    try:
        n1, add1, mul1 = R1
        n2, add2, mul2 = R2
        n = n1 * n2
        add = [[0]*n for _ in range(n)]
        mul = [[0]*n for _ in range(n)]
        for i1 in range(n1):
            for j1 in range(n2):
                for i2 in range(n1):
                    for j2 in range(n2):
                        idx1 = i1 * n2 + j1
                        idx2 = i2 * n2 + j2
                        add[idx1][idx2] = add1[i1][i2] * n2 + add2[j1][j2]
                        mul[idx1][idx2] = mul1[i1][i2] * n2 + mul2[j1][j2]
        return (n, add, mul)
    except Exception:
        return None

def direct_product_groups(G1, G2):
    try:
        if G1 is None or G2 is None:
            return None
        n1 = len(G1)
        n2 = len(G2)
        table = [[0]*(n1*n2) for _ in range(n1*n2)]
        for i1 in range(n1):
            for j1 in range(n2):
                for i2 in range(n1):
                    for j2 in range(n2):
                        idx1 = i1 * n2 + j1
                        idx2 = i2 * n2 + j2
                        prod1 = G1[i1][i2]
                        prod2 = G2[j1][j2]
                        table[idx1][idx2] = prod1 * n2 + prod2
        return table
    except Exception:
        return None

def are_isomorphic(G1, G2):
    try:
        if G1 is None or G2 is None:
            return False
        n = len(G1)
        if len(G2) != n:
            return False
        if n == 0:
            return True
        
        def find_id(G):
            for i in range(n):
                if all(G[i][j] == j for j in range(n)): return i
            return None
        e1 = find_id(G1)
        e2 = find_id(G2)
        if e1 is None or e2 is None:
            return False
            
        def element_order(G, x, e):
            curr = x
            ord = 1
            while curr != e:
                curr = G[curr][x]
                ord += 1
                if ord > n:
                    return None
            return ord

        ords1 = [element_order(G1, i, e1) for i in range(n)]
        ords2 = [element_order(G2, i, e2) for i in range(n)]
        
        if any(o is None for o in ords1) or any(o is None for o in ords2):
            return False
            
        if sorted(ords1) != sorted(ords2):
            return False
            
        by_ord1 = {}
        by_ord2 = {}
        for i, o in enumerate(ords1):
            if o not in by_ord1: by_ord1[o] = []
            by_ord1[o].append(i)
        for i, o in enumerate(ords2):
            if o not in by_ord2: by_ord2[o] = []
            by_ord2[o].append(i)
        
        mapping = {}
        used = set()
        
        def backtrack(idx):
            if idx == n:
                for i in range(n):
                    for j in range(n):
                        if mapping[G1[i][j]] != G2[mapping[i]][mapping[j]]:
                            return False
                return True
                
            i = idx
            o = ords1[i]
            for j in by_ord2[o]:
                if j not in used:
                    mapping[i] = j
                    used.add(j)
                    
                    ok = True
                    for x in range(i + 1):
                        for y in range(i + 1):
                            xy = G1[x][y]
                            if xy <= i:
                                if mapping[xy] != G2[mapping[x]][mapping[y]]:
                                    ok = False
                                    break
                        if not ok: break
                    
                    if ok:
                        if backtrack(i + 1):
                            return True
                            
                    del mapping[i]
                    used.remove(j)
            return False

        return backtrack(0)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R1, R2 = witness
            if not (is_ring(R1) and is_ring(R2)):
                return [False, False, False]
            R3 = direct_product_ring(R1, R2)
            is_dp = True
        elif isinstance(witness, tuple) and len(witness) == 3:
            R1, R2, R3 = witness
            if not (is_ring(R1) and is_ring(R2) and is_ring(R3)):
                return [False, False, False]
            expected_R3 = direct_product_ring(R1, R2)
            is_dp = (R3 == expected_R3)
        else:
            return [False, False, False]
            
        h1 = get_identity(R2) is not None
        h2 = is_dp
        
        U_R1 = get_unit_group(R1)
        U_R2 = get_unit_group(R2)
        U_R3 = get_unit_group(R3)
        
        if U_R3 is None:
            neg_q = True
        else:
            U_R1_x_R2 = direct_product_groups(U_R1, U_R2)
            if U_R1_x_R2 is None:
                neg_q = True
            else:
                neg_q = not are_isomorphic(U_R3, U_R1_x_R2)
                
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R2 is a ring with multiplicative identity",
    "H_2: R1 x R2 is the direct product ring of R1 and R2",
    "¬Q: U(R1 x R2) is not isomorphic to U(R1) x U(R2)"
]

N_HYP = 2
NEG_Q_INDEX = 2