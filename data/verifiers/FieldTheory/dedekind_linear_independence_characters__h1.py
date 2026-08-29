import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

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

def conditions(witness):
    try:
        # Witness can be either (p, q, sigmas) for prime fields Z_p and Z_q
        # or (E_add, E_mul, F_add, F_mul, sigmas) for general finite fields
        if len(witness) == 3:
            p, q, sigmas = witness
            p, q = int(p), int(q)
            if p > 50 or q > 50:
                return [False, False]
            E_size, F_size = p, q
            E_add = [[(i + j) % p for j in range(p)] for i in range(p)]
            E_mul = [[(i * j) % p for j in range(p)] for i in range(p)]
            F_add = [[(i + j) % q for j in range(q)] for i in range(q)]
            F_mul = [[(i * j) % q for j in range(q)] for i in range(q)]
        elif len(witness) == 5:
            E_add, E_mul, F_add, F_mul, sigmas = witness
            E_size = len(E_add)
            F_size = len(F_add)
            if E_size > 50 or F_size > 50:
                return [False, False]
            E_add = [[int(x) for x in row] for row in E_add]
            E_mul = [[int(x) for x in row] for row in E_mul]
            F_add = [[int(x) for x in row] for row in F_add]
            F_mul = [[int(x) for x in row] for row in F_mul]
        else:
            return [False, False]
            
        for i in range(E_size):
            if len(E_add[i]) != E_size or len(E_mul[i]) != E_size:
                return [False, False]
            for j in range(E_size):
                if not (0 <= E_add[i][j] < E_size) or not (0 <= E_mul[i][j] < E_size):
                    return [False, False]
                    
        for i in range(F_size):
            if len(F_add[i]) != F_size or len(F_mul[i]) != F_size:
                return [False, False]
            for j in range(F_size):
                if not (0 <= F_add[i][j] < F_size) or not (0 <= F_mul[i][j] < F_size):
                    return [False, False]

        def is_field(add, mul, size):
            if size < 2: return False, -1, -1
            zero = -1
            for i in range(size):
                if all(add[i][j] == j and add[j][i] == j for j in range(size)):
                    zero = i
                    break
            if zero == -1: return False, -1, -1
            
            one = -1
            for i in range(size):
                if all(mul[i][j] == j and mul[j][i] == j for j in range(size)):
                    one = i
                    break
            if one == -1 or one == zero: return False, -1, -1
            
            for i in range(size):
                if not any(add[i][j] == zero for j in range(size)): return False, -1, -1
                
            for i in range(size):
                if i == zero: continue
                if not any(mul[i][j] == one for j in range(size)): return False, -1, -1
                
            for i in range(size):
                for j in range(size):
                    if add[i][j] != add[j][i]: return False, -1, -1
                    if mul[i][j] != mul[j][i]: return False, -1, -1
                    
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if add[add[i][j]][k] != add[i][add[j][k]]: return False, -1, -1
                        if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False, -1, -1
                        
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False, -1, -1
                        
            return True, zero, one

        is_E_field, E_zero, E_one = is_field(E_add, E_mul, E_size)
        is_F_field, F_zero, F_one = is_field(F_add, F_mul, F_size)
        
        if not is_E_field or not is_F_field:
            return [False, False]
            
        n = len(sigmas)
        if n < 1:
            return [False, False]
            
        normalized_sigmas = []
        for s in sigmas:
            if callable(s):
                normalized_sigmas.append([int(s(x)) for x in range(E_size)])
            elif isinstance(s, dict):
                normalized_sigmas.append([int(s[x]) for x in range(E_size)])
            else:
                normalized_sigmas.append([int(x) for x in s])
        sigmas = normalized_sigmas
            
        for s in sigmas:
            if len(s) != E_size:
                return [False, False]
            for x in s:
                if x < 0 or x >= F_size:
                    return [False, False]
                    
        unique_sigmas = set(tuple(s) for s in sigmas)
        if len(unique_sigmas) != n:
            return [False, False]
            
        is_homo = True
        for s in sigmas:
            for x in range(E_size):
                for y in range(E_size):
                    if s[E_add[x][y]] != F_add[s[x]][s[y]]:
                        is_homo = False
                    if s[E_mul[x][y]] != F_mul[s[x]][s[y]]:
                        is_homo = False
                        
        is_lin_dep = False
        for coeffs in product(range(F_size), repeat=n):
            if all(c == F_zero for c in coeffs):
                continue
            
            dep = True
            for x in range(E_size):
                val = F_zero
                for i in range(n):
                    term = F_mul[coeffs[i]][sigmas[i][x]]
                    val = F_add[val][term]
                if val != F_zero:
                    dep = False
                    break
            if dep:
                is_lin_dep = True
                break
                
        return [is_homo, is_lin_dep]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: sigma_1, ..., sigma_n are distinct field homomorphisms from E to F",
    "¬Q: The homomorphisms sigma_1, ..., sigma_n are linearly dependent over F"
]

N_HYP = 1
NEG_Q_INDEX = 1