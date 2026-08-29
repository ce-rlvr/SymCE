import sympy
from sympy import symbols, Rational, Integer

# Helper to generate addition and multiplication tables for Z_n
def make_Zn(n):
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return add, mul

# Pre-defined common finite rings for convenience
Z2_add, Z2_mul = make_Zn(2)
Z3_add, Z3_mul = make_Zn(3)
Z4_add, Z4_mul = make_Zn(4)
Z5_add, Z5_mul = make_Zn(5)
Z6_add, Z6_mul = make_Zn(6)

def is_ring(add, mul):
    try:
        n = len(add)
        if n == 0: return False
        if len(mul) != n: return False
        
        # Check dimensions and elements
        for row in list(add) + list(mul):
            if len(row) != n: return False
            for x in row:
                try:
                    x_int = int(x)
                    if x_int != x or not (0 <= x_int < n): return False
                except Exception:
                    return False
                
        # Additive identity (must be 0)
        for i in range(n):
            if int(add[i][0]) != i or int(add[0][i]) != i:
                return False
                
        # Additive inverse
        for i in range(n):
            if not any(int(add[i][j]) == 0 and int(add[j][i]) == 0 for j in range(n)):
                return False
                
        # Associativity and commutativity of add
        for i in range(n):
            for j in range(n):
                if int(add[i][j]) != int(add[j][i]): return False
                for k in range(n):
                    if int(add[int(add[i][j])][k]) != int(add[i][int(add[j][k])]): return False
                    
        # Associativity of mul
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if int(mul[int(mul[i][j])][k]) != int(mul[i][int(mul[j][k])]): return False
                    
        # Distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if int(mul[i][int(add[j][k])]) != int(add[int(mul[i][j])][int(mul[i][k])]): return False
                    if int(mul[int(add[i][j])][k]) != int(add[int(mul[i][k])][int(mul[j][k])]): return False
                    
        return True
    except Exception:
        return False

def is_ideal(add, mul, I):
    try:
        n = len(add)
        I_set = set()
        for x in I:
            x_int = int(x)
            if x_int != x or not (0 <= x_int < n): return False
            I_set.add(x_int)
            
        if not I_set: return False
        if 0 not in I_set: return False
            
        # Closed under addition
        for x in I_set:
            for y in I_set:
                if int(add[x][y]) not in I_set: return False
                
        # Closed under additive inverse
        for x in I_set:
            inv_x = next((y for y in range(n) if int(add[x][y]) == 0), None)
            if inv_x is None or inv_x not in I_set: return False
            
        # Closed under multiplication by any ring element (two-sided)
        for x in I_set:
            for r in range(n):
                if int(mul[r][x]) not in I_set: return False
                if int(mul[x][r]) not in I_set: return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness can be a dictionary, an object, or a tuple containing:
    (R_add, R_mul, S_add, S_mul, I, f)
    where R_add, R_mul are n x n lists representing the ring R,
    S_add, S_mul are m x m lists representing the ring S,
    I is a list of elements in R,
    f is a list, dict, or callable mapping elements of R to S.
    """
    try:
        if isinstance(witness, dict):
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            I = witness['I']
            f = witness['f']
        elif hasattr(witness, 'R_add'):
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            I = witness.I
            f = witness.f
        else:
            R_add, R_mul, S_add, S_mul, I, f = witness
            
        n_R = len(R_add)
        n_S = len(S_add)
        
        f_list = []
        for i in range(n_R):
            if isinstance(f, dict):
                val = f[i]
            elif callable(f):
                val = f(i)
            else:
                val = f[i]
            val_int = int(val)
            if not (0 <= val_int < n_S):
                return [False, False, False]
            f_list.append(val_int)
            
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are rings
    try:
        h1 = is_ring(R_add, R_mul) and is_ring(S_add, S_mul)
    except Exception:
        h1 = False
        
    # H_2: I is an ideal of R
    try:
        h2 = is_ideal(R_add, R_mul, I)
    except Exception:
        h2 = False
        
    # ¬Q: The preimage f^{-1}(f(I)) is not equal to the ideal I + ker(f)
    # This means either they are not equal as sets, OR I + ker(f) is not an ideal.
    try:
        ker_f = [x for x in range(n_R) if f_list[x] == 0]
        I_plus_ker = set(int(R_add[int(a)][b]) for a in I for b in ker_f)
        
        f_I = set(f_list[int(x)] for x in I)
        preimage = set(x for x in range(n_R) if f_list[x] in f_I)
        
        is_I_plus_ker_ideal = is_ideal(R_add, R_mul, list(I_plus_ker))
        sets_equal = (preimage == I_plus_ker)
        
        q = is_I_plus_ker_ideal and sets_equal
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: I is an ideal of R",
    "¬Q: The preimage f^{-1}(f(I)) is not equal to the ideal I + ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2