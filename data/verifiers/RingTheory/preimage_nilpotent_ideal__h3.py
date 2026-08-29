import operator
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: ker(f) is a nilpotent ideal of R",
    "¬Q: The preimage f^{-1}(N) is not a nilpotent ideal of R"
]
N_HYP = 3
NEG_Q_INDEX = 3

def find_zero(size, add):
    for i in range(size):
        if all(add[i][j] == j for j in range(size)) and all(add[j][i] == j for j in range(size)):
            return i
    return -1

def is_ring(size, add, mul, zero_idx):
    if size <= 0: return False
    if zero_idx < 0 or zero_idx >= size: return False
    # check closure
    for i in range(size):
        for j in range(size):
            if not (0 <= add[i][j] < size): return False
            if not (0 <= mul[i][j] < size): return False
    # check add commutativity
    for i in range(size):
        for j in range(size):
            if add[i][j] != add[j][i]: return False
    # check add associativity
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
    # check add identity
    for i in range(size):
        if add[i][zero_idx] != i or add[zero_idx][i] != i: return False
    # check add inverse
    for i in range(size):
        has_inv = False
        for j in range(size):
            if add[i][j] == zero_idx:
                has_inv = True
                break
        if not has_inv: return False
    # check mul associativity
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
    # check distributivity
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
    return True

def is_ideal(size, add, mul, zero_idx, I):
    I_set = set(I)
    if zero_idx not in I_set: return False
    # closed under add
    for x in I_set:
        for y in I_set:
            if add[x][y] not in I_set: return False
    # closed under mul by R
    for x in I_set:
        for r in range(size):
            if mul[x][r] not in I_set: return False
            if mul[r][x] not in I_set: return False
    # check additive inverse
    for x in I_set:
        inv_found = False
        for y in I_set:
            if add[x][y] == zero_idx:
                inv_found = True
                break
        if not inv_found: return False
    return True

def ideal_mul(size, add, mul, zero_idx, I, J):
    products = set()
    for x in I:
        for y in J:
            products.add(mul[x][y])
    
    closure = set(products)
    if zero_idx not in closure:
        closure.add(zero_idx)
    queue = list(closure)
    while queue:
        curr = queue.pop(0)
        for p in products:
            nxt = add[curr][p]
            if nxt not in closure:
                closure.add(nxt)
                queue.append(nxt)
    return closure

def is_nilpotent_ideal(size, add, mul, zero_idx, I):
    if not is_ideal(size, add, mul, zero_idx, I):
        return False
    curr_power = set(I)
    seen = []
    while True:
        if not curr_power or curr_power == {zero_idx}:
            return True
        if curr_power in seen:
            return False
        seen.append(curr_power)
        curr_power = ideal_mul(size, add, mul, zero_idx, curr_power, I)

def is_homomorphism(R_size, S_size, R_add, R_mul, S_add, S_mul, f):
    if len(f) != R_size: return False
    for x in f:
        if not (0 <= x < S_size): return False
    for i in range(R_size):
        for j in range(R_size):
            if f[R_add[i][j]] != S_add[f[i]][f[j]]: return False
            if f[R_mul[i][j]] != S_mul[f[i]][f[j]]: return False
    return True

def get_kernel(R_size, f, S_zero_idx):
    return [i for i in range(R_size) if f[i] == S_zero_idx]

def get_preimage(R_size, f, N):
    N_set = set(N)
    return [i for i in range(R_size) if f[i] in N_set]

def parse_witness(witness):
    # Case 1: Dictionary with tables
    if isinstance(witness, dict) and 'R_size' in witness:
        R_size = int(witness['R_size'])
        S_size = int(witness['S_size'])
        R_add = witness['R_add']
        R_mul = witness['R_mul']
        S_add = witness['S_add']
        S_mul = witness['S_mul']
        f = witness['f']
        N = witness['N']
        if not isinstance(N, (list, tuple, set)):
            N = [N]
        R_zero = find_zero(R_size, R_add)
        S_zero = find_zero(S_size, S_add)
        return (R_size, S_size, R_add, R_mul, S_add, S_mul, f, N, R_zero, S_zero)
    
    # Case 2: Tuple with tables (length 8)
    if isinstance(witness, (tuple, list)) and len(witness) == 8 and isinstance(witness[0], int):
        R_size, S_size, R_add, R_mul, S_add, S_mul, f, N = witness
        if not isinstance(N, (list, tuple, set)):
            N = [N]
        R_zero = find_zero(R_size, R_add)
        S_zero = find_zero(S_size, S_add)
        return (R_size, S_size, R_add, R_mul, S_add, S_mul, f, N, R_zero, S_zero)
        
    # Case 3: Object or dict with elements and functions
    if isinstance(witness, dict) and 'R' in witness:
        R = witness['R']
        S = witness['S']
        f_map = witness['f']
        N_elems = witness['N']
        R_add_func = witness.get('add_R', operator.add)
        R_mul_func = witness.get('mul_R', operator.mul)
        S_add_func = witness.get('add_S', operator.add)
        S_mul_func = witness.get('mul_S', operator.mul)
    elif hasattr(witness, 'R'):
        R = witness.R
        S = witness.S
        f_map = witness.f
        N_elems = witness.N
        R_add_func = getattr(witness, 'add_R', operator.add)
        R_mul_func = getattr(witness, 'mul_R', operator.mul)
        S_add_func = getattr(witness, 'add_S', operator.add)
        S_mul_func = getattr(witness, 'mul_S', operator.mul)
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        R, S, f_map, N_elems = witness
        R_add_func = operator.add
        R_mul_func = operator.mul
        S_add_func = operator.add
        S_mul_func = operator.mul
    else:
        raise ValueError("Unknown witness format")

    R_list = list(R)
    S_list = list(S)
    R_size = len(R_list)
    S_size = len(S_list)
    
    def index_of(lst, item):
        for i, x in enumerate(lst):
            if x == item:
                return i
        raise ValueError(f"Item not found: {item}")

    R_add = [[0]*R_size for _ in range(R_size)]
    R_mul = [[0]*R_size for _ in range(R_size)]
    for i, x in enumerate(R_list):
        for j, y in enumerate(R_list):
            R_add[i][j] = index_of(R_list, R_add_func(x, y))
            R_mul[i][j] = index_of(R_list, R_mul_func(x, y))
            
    S_add = [[0]*S_size for _ in range(S_size)]
    S_mul = [[0]*S_size for _ in range(S_size)]
    for i, x in enumerate(S_list):
        for j, y in enumerate(S_list):
            S_add[i][j] = index_of(S_list, S_add_func(x, y))
            S_mul[i][j] = index_of(S_list, S_mul_func(x, y))
            
    if isinstance(f_map, dict):
        f = [index_of(S_list, f_map[x]) for x in R_list]
    elif callable(f_map):
        f = [index_of(S_list, f_map(x)) for x in R_list]
    elif isinstance(f_map, (list, tuple)) and len(f_map) > 0 and isinstance(f_map[0], (list, tuple)) and len(f_map[0]) == 2:
        f = []
        for x in R_list:
            found = False
            for k, v in f_map:
                if k == x:
                    f.append(index_of(S_list, v))
                    found = True
                    break
            if not found:
                raise ValueError(f"Mapping for {x} not found")
    else:
        f = [index_of(S_list, y) for y in f_map]
        
    if not isinstance(N_elems, (list, tuple, set)):
        N_elems = [N_elems]
    N = [index_of(S_list, y) for y in N_elems]
    
    R_zero = find_zero(R_size, R_add)
    S_zero = find_zero(S_size, S_add)
    
    return (R_size, S_size, R_add, R_mul, S_add, S_mul, f, N, R_zero, S_zero)

def conditions(witness):
    try:
        parsed = parse_witness(witness)
        if parsed is None:
            return [False, False, False, False]
        R_size, S_size, R_add, R_mul, S_add, S_mul, f, N, R_zero, S_zero = parsed
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    try:
        h1 = is_ring(R_size, R_add, R_mul, R_zero) and is_ring(S_size, S_add, S_mul, S_zero)
    except Exception:
        h1 = False

    # H2: f is a ring homomorphism
    try:
        h2 = is_homomorphism(R_size, S_size, R_add, R_mul, S_add, S_mul, f)
    except Exception:
        h2 = False

    # H3: ker(f) is a nilpotent ideal of R
    try:
        ker = get_kernel(R_size, f, S_zero)
        h3 = is_nilpotent_ideal(R_size, R_add, R_mul, R_zero, ker)
    except Exception:
        h3 = False

    # neg_Q: f^{-1}(N) is NOT a nilpotent ideal of R
    try:
        N_valid = all(0 <= x < S_size for x in N)
        if not N_valid:
            neg_q = False
        else:
            preimage = get_preimage(R_size, f, N)
            neg_q = not is_nilpotent_ideal(R_size, R_add, R_mul, R_zero, preimage)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]