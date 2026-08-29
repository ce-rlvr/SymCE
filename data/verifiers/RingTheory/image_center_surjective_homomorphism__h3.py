import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "¬Q: The image f(Z(R)) is not contained in the center of S"
]

def is_ring(add, mul):
    n = len(add)
    if n == 0: 
        return False
    if len(mul) != n: 
        return False
    for row in add:
        if len(row) != n: 
            return False
    for row in mul:
        if len(row) != n: 
            return False

    # Commutativity of addition
    for i in range(n):
        for j in range(i, n):
            if add[i][j] != add[j][i]: 
                return False

    # Associativity and Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: 
                    return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: 
                    return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: 
                    return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: 
                    return False

    # Identity and inverses for addition
    has_zero = False
    for z in range(n):
        if all(add[z][i] == i for i in range(n)):
            inv_ok = True
            for i in range(n):
                if not any(add[i][j] == z for j in range(n)):
                    inv_ok = False
                    break
            if inv_ok:
                has_zero = True
                break
                
    if not has_zero: 
        return False

    return True

def is_homomorphism(R_add, R_mul, S_add, S_mul, f):
    n = len(R_add)
    m = len(S_add)
    
    for i in range(n):
        try:
            fi = f[i]
        except (KeyError, IndexError):
            return False
        if not (0 <= fi < m): 
            return False
        
    for i in range(n):
        for j in range(n):
            if f[R_add[i][j]] != S_add[f[i]][f[j]]: 
                return False
            if f[R_mul[i][j]] != S_mul[f[i]][f[j]]: 
                return False
            
    return True

def is_surjective(f, m):
    if isinstance(f, dict):
        vals = f.values()
    else:
        vals = f
    return len(set(vals)) == m

def get_center(mul):
    n = len(mul)
    center = []
    for i in range(n):
        if all(mul[i][j] == mul[j][i] for j in range(n)):
            center.append(i)
    return center

def conditions(witness):
    try:
        # Extract Cayley tables and mapping
        if isinstance(witness, dict):
            R_add = witness["R_add"]
            R_mul = witness["R_mul"]
            S_add = witness["S_add"]
            S_mul = witness["S_mul"]
            f = witness["f"]
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            R_add, R_mul, S_add, S_mul, f = witness
        else:
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            f = witness.f
            
        # H1: R and S are rings
        h1 = is_ring(R_add, R_mul) and is_ring(S_add, S_mul)
        
        # H2: f is a surjective ring homomorphism
        h2 = is_homomorphism(R_add, R_mul, S_add, S_mul, f) and is_surjective(f, len(S_add))
        
        # ¬Q: The image f(Z(R)) is NOT contained in the center of S
        Z_R = get_center(R_mul)
        Z_S = get_center(S_mul)
        
        f_Z_R = set(f[x] for x in Z_R)
        neg_q = not f_Z_R.issubset(set(Z_S))
        
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]