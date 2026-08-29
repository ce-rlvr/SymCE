import itertools

# Top-level setup
# (No specific named objects required for this Boolean ring counterexample, 
# as the witness is expected to be an integer or a tuple defining the ring tables)

def is_boolean_ring_with_identity(n, add, mul):
    if not isinstance(n, int) or n <= 0: return False
    if len(add) != n or any(len(row) != n for row in add): return False
    if len(mul) != n or any(len(row) != n for row in mul): return False
    
    # Check closure
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False

    # Check addition abelian group
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False

    for i in range(n):
        for j in range(n):
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

    # Check multiplication associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False

    # Check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False

    # Check Boolean (idempotent)
    for i in range(n):
        if mul[i][i] != i: return False

    # Check Identity
    identity = -1
    for i in range(n):
        if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
            identity = i
            break
    if identity == -1: return False
    
    return True

def conditions(witness):
    try:
        # The witness can be just the element x (assuming R = Z/2Z)
        # or a full tuple (n, add_table, mul_table, x) defining the ring and the element.
        if isinstance(witness, (tuple, list)) and len(witness) == 4 and isinstance(witness[1], (tuple, list)):
            n, add_table, mul_table, x = witness
            n = int(n)
            x = int(x)
        else:
            x = int(witness)
            n = 2
            add_table = [[0, 1], [1, 0]]
            mul_table = [[0, 0], [0, 1]]
            
        h1_ok = False
        if 0 < n <= 16 and 0 <= x < n:
            h1_ok = is_boolean_ring_with_identity(n, add_table, mul_table)
    except Exception:
        h1_ok = False
        n = 0

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            identity = -1
            for i in range(n):
                if all(mul_table[i][j] == j and mul_table[j][i] == j for j in range(n)):
                    identity = i
                    break
            
            exists_homo = False
            # Iterate over all possible functions f: R -> Z/2Z
            for f in itertools.product([0, 1], repeat=n):
                if f[x] != 1:
                    continue
                
                # A ring homomorphism from a ring with identity must map 1_R to 1_S
                if identity != -1 and f[identity] != 1:
                    continue
                    
                is_homo = True
                for i in range(n):
                    for j in range(n):
                        if f[add_table[i][j]] != (f[i] + f[j]) % 2:
                            is_homo = False
                            break
                        if f[mul_table[i][j]] != (f[i] * f[j]) % 2:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                
                if is_homo:
                    exists_homo = True
                    break
                    
            neg_q_ok = not exists_homo
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity",
    "¬Q: There does not exist a ring homomorphism f: R -> Z/2Z such that f(x) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1