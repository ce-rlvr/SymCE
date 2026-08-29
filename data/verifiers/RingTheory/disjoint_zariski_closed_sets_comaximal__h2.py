import itertools

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "¬Q: The conclusion 'I and J are comaximal iff V(I) \\cap V(J) is empty' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        # Witness is expected to be a tuple: (n, add_table, mult_table, I, J)
        # where n is the size of the ring, add_table and mult_table are n x n lists,
        # and I, J are lists of elements representing the ideals.
        n, add_table, mult_table, I, J = witness
        
        if not isinstance(n, int) or n <= 0 or n > 10:
            return [False, False, False]
            
        if len(add_table) != n or any(len(row) != n for row in add_table):
            return [False, False, False]
        if len(mult_table) != n or any(len(row) != n for row in mult_table):
            return [False, False, False]
            
        is_comm_ring = True
        for row in add_table:
            for val in row:
                if not isinstance(val, int) or not (0 <= val < n):
                    is_comm_ring = False
        for row in mult_table:
            for val in row:
                if not isinstance(val, int) or not (0 <= val < n):
                    is_comm_ring = False
                    
        if not is_comm_ring:
            return [False, False, False]

        # Commutativity
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]:
                    is_comm_ring = False
                if mult_table[i][j] != mult_table[j][i]:
                    is_comm_ring = False
                    
        # Associativity and Distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                        is_comm_ring = False
                    if mult_table[mult_table[i][j]][k] != mult_table[i][mult_table[j][k]]:
                        is_comm_ring = False
                    if mult_table[i][add_table[j][k]] != add_table[mult_table[i][j]][mult_table[i][k]]:
                        is_comm_ring = False
                        
        # Additive Identity
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            is_comm_ring = False
        else:
            # Additive Inverses
            for i in range(n):
                if zero not in add_table[i]:
                    is_comm_ring = False
                    
        h1 = is_comm_ring
        
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    try:
        def is_ideal(S):
            if not S: return False
            for x in S:
                for y in S:
                    if add_table[x][y] not in S: return False
            for x in S:
                for r in range(n):
                    if mult_table[r][x] not in S: return False
            if zero not in S: return False
            for x in S:
                inv = -1
                for y in range(n):
                    if add_table[x][y] == zero:
                        inv = y
                        break
                if inv not in S: return False
            return True

        I_set = set(I)
        J_set = set(J)
        
        if all(isinstance(x, int) and 0 <= x < n for x in I_set) and \
           all(isinstance(x, int) and 0 <= x < n for x in J_set):
            h2 = is_ideal(I_set) and is_ideal(J_set)
        else:
            h2 = False
            
    except Exception:
        h2 = False

    if not h2:
        return [h1, False, False]

    try:
        def is_prime_ideal(S):
            if not is_ideal(S): return False
            if len(S) == n: return False
            for a in range(n):
                for b in range(n):
                    if mult_table[a][b] in S:
                        if a not in S and b not in S:
                            return False
            return True

        prime_ideals = []
        for r in range(1, n):
            for subset in itertools.combinations(range(n), r):
                S = set(subset)
                if is_prime_ideal(S):
                    prime_ideals.append(S)
                    
        V_I = [P for P in prime_ideals if I_set.issubset(P)]
        V_J = [P for P in prime_ideals if J_set.issubset(P)]
        
        V_I_cap_V_J = [P for P in V_I if P in V_J]
        is_empty = (len(V_I_cap_V_J) == 0)
        
        I_plus_J = set()
        for x in I_set:
            for y in J_set:
                I_plus_J.add(add_table[x][y])
                
        is_comaximal = (len(I_plus_J) == n)
        
        neg_q = (is_comaximal != is_empty)
        
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]