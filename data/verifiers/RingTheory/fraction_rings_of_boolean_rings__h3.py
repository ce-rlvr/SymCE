import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# (No specific named bindings required for finite rings, but we provide standard symbols)

def extract_witness(witness):
    if isinstance(witness, dict):
        if 'add' in witness and 'mul' in witness and 'S' in witness:
            R_add, R_mul, S = witness['add'], witness['mul'], witness['S']
        elif 'R_add' in witness and 'R_mul' in witness and 'S' in witness:
            R_add, R_mul, S = witness['R_add'], witness['R_mul'], witness['S']
        else:
            raise ValueError("Dict missing required keys")
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        R_add, R_mul, S = witness[0], witness[1], witness[2]
    elif hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'S'):
        R_add, R_mul, S = witness.add, witness.mul, witness.S
    elif hasattr(witness, 'R_add') and hasattr(witness, 'R_mul') and hasattr(witness, 'S'):
        R_add, R_mul, S = witness.R_add, witness.R_mul, witness.S
    else:
        raise ValueError("Unknown witness format")
        
    R_add = [[int(val) for val in row] for row in R_add]
    R_mul = [[int(val) for val in row] for row in R_mul]
    S = [int(val) for val in S]
    return R_add, R_mul, S

def is_boolean_ring(R_add, R_mul):
    n = len(R_add)
    if n == 0: return False
    
    for i in range(n):
        if len(R_add[i]) != n or len(R_mul[i]) != n: return False
        for j in range(n):
            if R_add[i][j] < 0 or R_add[i][j] >= n: return False
            if R_mul[i][j] < 0 or R_mul[i][j] >= n: return False
            
    zero = None
    for i in range(n):
        if all(R_add[i][j] == j for j in range(n)) and all(R_add[j][i] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    
    for i in range(n):
        has_inv = False
        for j in range(n):
            if R_add[i][j] == zero and R_add[j][i] == zero:
                has_inv = True
            if R_add[i][j] != R_add[j][i]: return False
        if not has_inv: return False
        
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: return False
                if R_mul[R_add[i][j]][k] != R_add[R_mul[i][k]][R_mul[j][k]]: return False
                
    for i in range(n):
        if R_mul[i][i] != i: return False
        
    one = None
    for i in range(n):
        if all(R_mul[i][j] == j for j in range(n)) and all(R_mul[j][i] == j for j in range(n)):
            one = i
            break
    if one is None: return False
    if one == zero: return False
    
    return True

def check_localization_is_boolean_ring(R_add, R_mul, S):
    n = len(R_add)
    if not S:
        return False
        
    zero = None
    for i in range(n):
        if all(R_add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None:
        return False
        
    inv = [None] * n
    for i in range(n):
        for j in range(n):
            if R_add[i][j] == zero and R_add[j][i] == zero:
                inv[i] = j
                break
        if inv[i] is None:
            return False
            
    pairs = [(r, s) for r in range(n) for s in S]
    
    def equiv(p1, p2):
        r1, s1 = p1
        r2, s2 = p2
        term1 = R_mul[r1][s2]
        term2 = R_mul[r2][s1]
        diff = R_add[term1][inv[term2]]
        for u in S:
            if R_mul[u][diff] == zero:
                return True
        return False

    classes = []
    for p in pairs:
        found = False
        for c in classes:
            if equiv(p, c[0]):
                c.append(p)
                found = True
                break
        if not found:
            classes.append([p])
            
    num_classes = len(classes)
    if num_classes == 0:
        return False
        
    def get_class(p):
        for i, c in enumerate(classes):
            if equiv(p, c[0]):
                return i
        return -1
        
    loc_add = [[0]*num_classes for _ in range(num_classes)]
    loc_mul = [[0]*num_classes for _ in range(num_classes)]
    
    for i in range(num_classes):
        for j in range(num_classes):
            r1, s1 = classes[i][0]
            r2, s2 = classes[j][0]
            
            num_a = R_add[R_mul[r1][s2]][R_mul[r2][s1]]
            den_a = R_mul[s1][s2]
            idx_a = get_class((num_a, den_a))
            if idx_a == -1: return False
            loc_add[i][j] = idx_a
            
            num_m = R_mul[r1][r2]
            den_m = R_mul[s1][s2]
            idx_m = get_class((num_m, den_m))
            if idx_m == -1: return False
            loc_mul[i][j] = idx_m
            
    return is_boolean_ring(loc_add, loc_mul)

def conditions(witness):
    try:
        R_add, R_mul, S = extract_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_boolean_ring(R_add, R_mul)
    except Exception:
        h1_ok = False
        
    try:
        n = len(R_add)
        h2_ok = True
        if not all(0 <= s < n for s in S):
            h2_ok = False
        else:
            for s1 in S:
                for s2 in S:
                    if R_mul[s1][s2] not in S:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False
        
    try:
        neg_q_ok = not check_localization_is_boolean_ring(R_add, R_mul, S)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^-1 R is not a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2