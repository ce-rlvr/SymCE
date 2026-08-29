import itertools
import sympy
from sympy import symbols

# Top-level setup for potential symbolic witnesses
x, y, z = symbols('x y z')

# Expected witness format:
# witness = {
#     "R_n": int,                        # Number of elements in R
#     "R_add": list[list[int]],          # Addition Cayley table for R
#     "R_mul": list[list[int]],          # Multiplication Cayley table for R
#     "S_n": int,                        # Number of elements in S
#     "S_add": list[list[int]],          # Addition Cayley table for S
#     "S_mul": list[list[int]],          # Multiplication Cayley table for S
#     "f": list[int],                    # Mapping from R to S (index to index)
#     "N": list[int]                     # Elements of the ideal N in S
# }

def get_zero(add, n):
    for e in range(n):
        if all(add[e][a] == a for a in range(n)):
            return e
    return None

def get_one(mul, n):
    for e in range(n):
        if all(mul[e][a] == a and mul[a][e] == a for a in range(n)):
            return e
    return None

def is_ring(n, add, mul):
    if n <= 0: return False
    if len(add) != n or any(len(row) != n for row in add): return False
    if len(mul) != n or any(len(row) != n for row in mul): return False
    
    # Addition associativity
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if add[add[a][b]][c] != add[a][add[b][c]]: return False
                
    # Addition commutativity
    for a in range(n):
        for b in range(n):
            if add[a][b] != add[b][a]: return False
            
    zero = get_zero(add, n)
    if zero is None: return False
    
    # Additive inverses
    for a in range(n):
        if not any(add[a][b] == zero for b in range(n)): return False
        
    # Multiplication associativity
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return False
                
    # Distributivity
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
                if mul[add[a][b]][c] != add[mul[a][c]][mul[b][c]]: return False
                
    # Multiplicative identity
    one = get_one(mul, n)
    if one is None: return False
    
    return True

def additive_closure(subset, add, n, zero):
    closure = set(subset)
    closure.add(zero)
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for a in closure:
            for b in closure:
                c = add[a][b]
                if c not in closure:
                    new_elements.add(c)
        if new_elements:
            closure.update(new_elements)
            changed = True
    return closure

def ideal_multiply(A, B, add, mul, n, zero):
    products = set()
    for a in A:
        for b in B:
            products.add(mul[a][b])
    return additive_closure(products, add, n, zero)

def is_ideal(N_set, add, mul, n, zero):
    if not N_set: return False
    if zero not in N_set: return False
    
    # Additive closure
    for a in N_set:
        for b in N_set:
            if add[a][b] not in N_set: return False
            
    # Absorption
    for a in N_set:
        for r in range(n):
            if mul[a][r] not in N_set: return False
            if mul[r][a] not in N_set: return False
            
    return True

def is_nilpotent_ideal(N_set, add, mul, n, zero):
    if not is_ideal(N_set, add, mul, n, zero):
        return False
    
    current_I = set(N_set)
    while True:
        if not current_I or current_I == {zero}:
            return True
        next_I = ideal_multiply(current_I, N_set, add, mul, n, zero)
        if next_I == current_I:
            return False
        current_I = next_I

def is_homomorphism(f, R_add, R_mul, R_n, S_add, S_mul, S_n):
    if len(f) != R_n: return False
    for a in range(R_n):
        if f[a] < 0 or f[a] >= S_n: return False
        
    for a in range(R_n):
        for b in range(R_n):
            if f[R_add[a][b]] != S_add[f[a]][f[b]]: return False
            if f[R_mul[a][b]] != S_mul[f[a]][f[b]]: return False
            
    R_1 = get_one(R_mul, R_n)
    S_1 = get_one(S_mul, S_n)
    if R_1 is not None and S_1 is not None:
        if f[R_1] != S_1: return False
        
    return True

def conditions(witness):
    try:
        R_n = witness["R_n"]
        R_add = witness["R_add"]
        R_mul = witness["R_mul"]
        
        S_n = witness["S_n"]
        S_add = witness["S_add"]
        S_mul = witness["S_mul"]
        
        f = witness["f"]
        N = set(witness["N"])
        
        # H_1: R is a ring
        h1 = is_ring(R_n, R_add, R_mul)
        
        # H_2: S is a ring
        h2 = is_ring(S_n, S_add, S_mul)
        
        # H_3: f is a ring homomorphism
        h3 = is_homomorphism(f, R_add, R_mul, R_n, S_add, S_mul, S_n)
        
        # H_4: N is a nilpotent ideal of S
        if any(x < 0 or x >= S_n for x in N):
            h4 = False
        else:
            S_zero = get_zero(S_add, S_n)
            if S_zero is not None:
                h4 = is_nilpotent_ideal(N, S_add, S_mul, S_n, S_zero)
            else:
                h4 = False
                
        # ¬Q: f^{-1}(N) is NOT a nilpotent ideal of R
        R_zero = get_zero(R_add, R_n)
        if R_zero is not None and len(f) == R_n and all(0 <= f[a] < S_n for a in range(R_n)):
            preimage_N = set(a for a in range(R_n) if f[a] in N)
            neg_q = not is_nilpotent_ideal(preimage_N, R_add, R_mul, R_n, R_zero)
        else:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: S is a ring",
    "H_3: f is a ring homomorphism from R to S",
    "H_4: N is a nilpotent ideal of S",
    "¬Q: f^{-1}(N) is not a nilpotent ideal of R"
]

N_HYP = 4
NEG_Q_INDEX = 4