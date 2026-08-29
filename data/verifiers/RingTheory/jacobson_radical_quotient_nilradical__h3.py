import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_zero(n, add):
    for i in range(n):
        if all(add[i][j] == j for j in range(n)) and all(add[j][i] == j for j in range(n)):
            return i
    return None

def is_commutative_ring(n, add, mul):
    if not isinstance(n, int) or n <= 0: return False
    if not isinstance(add, list) or len(add) != n: return False
    if not isinstance(mul, list) or len(mul) != n: return False
    for row in add:
        if not isinstance(row, list) or len(row) != n: return False
    for row in mul:
        if not isinstance(row, list) or len(row) != n: return False
        
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

    zero = get_zero(n, add)
    if zero is None: return False

    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False

    return True

def is_nilpotent(x, n, mul, zero):
    curr = x
    for _ in range(n):
        if curr == zero:
            return True
        curr = mul[curr][x]
    return False

def get_nilradical(n, add, mul):
    zero = get_zero(n, add)
    N = []
    for i in range(n):
        if is_nilpotent(i, n, mul, zero):
            N.append(i)
    return set(N)

def is_ideal(n, add, mul, N_list):
    if not all(isinstance(x, int) and 0 <= x < n for x in N_list):
        return False
    zero = get_zero(n, add)
    if zero not in N_list: return False
    N_set = set(N_list)
    for x in N_list:
        for y in N_list:
            neg_y = None
            for i in range(n):
                if add[y][i] == zero:
                    neg_y = i
                    break
            if neg_y is None: return False
            if add[x][neg_y] not in N_set: return False
    for x in N_list:
        for r in range(n):
            if mul[r][x] not in N_set: return False
            if mul[x][r] not in N_set: return False
    return True

def get_coset_rep(x, n, add, N_list, zero):
    coset = set()
    for y in N_list:
        coset.add(add[x][y])
    return min(coset)

def get_quotient_ring(n, add, mul, N_list):
    zero = get_zero(n, add)
    reps = set()
    for i in range(n):
        reps.add(get_coset_rep(i, n, add, N_list, zero))
    reps = sorted(list(reps))
    
    m = len(reps)
    rep_to_idx = {rep: i for i, rep in enumerate(reps)}
    
    q_add = [[0]*m for _ in range(m)]
    q_mul = [[0]*m for _ in range(m)]
    
    for i in range(m):
        for j in range(m):
            sum_val = add[reps[i]][reps[j]]
            sum_rep = get_coset_rep(sum_val, n, add, N_list, zero)
            q_add[i][j] = rep_to_idx[sum_rep]
            
            prod_val = mul[reps[i]][reps[j]]
            prod_rep = get_coset_rep(prod_val, n, add, N_list, zero)
            q_mul[i][j] = rep_to_idx[prod_rep]
            
    return m, q_add, q_mul, reps, rep_to_idx

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            N_list = witness.get("N")
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                R, N_list = witness
            elif len(witness) == 4:
                n, add, mul, N_list = witness
                R = (n, add, mul)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if not isinstance(R, tuple) or len(R) != 3:
            return [False, False, False]
            
        n, add, mul = R
        if not isinstance(N_list, (list, tuple, set)):
            return [False, False, False]
        N_list = list(N_list)
    except Exception:
        return [False, False, False]

    try:
        H1 = is_commutative_ring(n, add, mul)
    except Exception:
        H1 = False

    try:
        actual_N = get_nilradical(n, add, mul)
        H2 = (set(N_list) == actual_N)
    except Exception:
        H2 = False

    try:
        zero = get_zero(n, add)
        if zero is None or not is_ideal(n, add, mul, N_list):
            neg_Q = False
        else:
            m, q_add, q_mul, reps, rep_to_idx = get_quotient_ring(n, add, mul, N_list)
            J_RN_idx = get_nilradical(m, q_add, q_mul)
            J_RN = set(reps[i] for i in J_RN_idx)
            
            J_R = get_nilradical(n, add, mul)
            J_over_N = set()
            for x in J_R:
                J_over_N.add(get_coset_rep(x, n, add, N_list, zero))
                
            neg_Q = (J_RN != J_over_N)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: N is the nilradical of R",
    "¬Q: The Jacobson radical of the quotient ring R/N is not equal to J/N"
]

N_HYP = 2
NEG_Q_INDEX = 2