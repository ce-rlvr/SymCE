import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_commutative_ring_with_identity(n, add_table, mul_table):
    if not (isinstance(n, int) and n > 0): return False
    if len(add_table) != n or len(mul_table) != n: return False
    for i in range(n):
        if len(add_table[i]) != n or len(mul_table[i]) != n: return False
        for j in range(n):
            if not (isinstance(add_table[i][j], int) and 0 <= add_table[i][j] < n): return False
            if not (isinstance(mul_table[i][j], int) and 0 <= mul_table[i][j] < n): return False

    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False

    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False

    for i in range(n):
        if not any(add_table[i][j] == zero for j in range(n)): return False

    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]: return False

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False

    one = None
    for i in range(n):
        if all(mul_table[i][j] == j for j in range(n)):
            one = i
            break
    if one is None: return False

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False

    return True

def generate_ideal(n, add_table, mul_table, generators):
    ideal = set(generators)
    if not ideal:
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                return {i}
    
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for x in ideal:
            for y in ideal:
                s = add_table[x][y]
                if s not in ideal and s not in new_elements:
                    new_elements.add(s)
            for r in range(n):
                p = mul_table[r][x]
                if p not in ideal and p not in new_elements:
                    new_elements.add(p)
        if new_elements:
            ideal.update(new_elements)
            changed = True
    return ideal

def product_ideal(n, add_table, mul_table, I, J):
    generators = set()
    for x in I:
        for y in J:
            generators.add(mul_table[x][y])
    return generate_ideal(n, add_table, mul_table, generators)

def radical_ideal(n, mul_table, I):
    radical = set()
    for x in range(n):
        p = x
        in_ideal = False
        if p in I:
            in_ideal = True
        else:
            for _ in range(n):
                p = mul_table[p][x]
                if p in I:
                    in_ideal = True
                    break
        if in_ideal:
            radical.add(x)
    return radical

def poly_mul(n, add_table, mul_table, f, g):
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
            
    if not f or not g:
        return [zero]
    
    deg_f = len(f) - 1
    deg_g = len(g) - 1
    deg_fg = deg_f + deg_g
    
    fg = [zero] * (deg_fg + 1)
    for i in range(len(f)):
        for j in range(len(g)):
            prod = mul_table[f[i]][g[j]]
            fg[i+j] = add_table[fg[i+j]][prod]
            
    while len(fg) > 1 and fg[-1] == zero:
        fg.pop()
        
    return fg

def conditions(witness):
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        n, add_table, mul_table, f_coeffs, g_coeffs = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_commutative_ring_with_identity(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = (isinstance(f_coeffs, list) and len(f_coeffs) > 0 and all(isinstance(c, int) and 0 <= c < n for c in f_coeffs) and
              isinstance(g_coeffs, list) and len(g_coeffs) > 0 and all(isinstance(c, int) and 0 <= c < n for c in g_coeffs))
    except Exception:
        h2 = False
        
    h3 = True
    
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            fg_coeffs = poly_mul(n, add_table, mul_table, f_coeffs, g_coeffs)
            
            c_f = generate_ideal(n, add_table, mul_table, f_coeffs)
            c_g = generate_ideal(n, add_table, mul_table, g_coeffs)
            c_fg = generate_ideal(n, add_table, mul_table, fg_coeffs)
            
            c_f_c_g = product_ideal(n, add_table, mul_table, c_f, c_g)
            
            rad_c_fg = radical_ideal(n, mul_table, c_fg)
            rad_c_f_c_g = radical_ideal(n, mul_table, c_f_c_g)
            
            neg_q = (rad_c_fg != rad_c_f_c_g)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f and g are polynomials over R",
    "H_3: c(h) denotes the ideal generated by the coefficients of a polynomial h",
    "not_Q: sqrt(c(fg)) != sqrt(c(f)c(g))"
]

N_HYP = 3
NEG_Q_INDEX = 3