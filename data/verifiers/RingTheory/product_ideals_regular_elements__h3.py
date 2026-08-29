import itertools

def get_zero(n, add):
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            return i
    return None

def is_commutative_ring(n, add, mul):
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
            
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    z = get_zero(n, add)
    if z is None: return False
    
    for i in range(n):
        if not any(add[i][j] == z for j in range(n)): return False
        
    return True

def is_ideal(n, add, mul, zero, S):
    if not S: return False
    S_set = set(S)
    if zero not in S_set: return False
    for x in S:
        for y in S:
            if add[x][y] not in S_set: return False
    for x in S:
        for r in range(n):
            if mul[x][r] not in S_set: return False
    return True

def is_regular(n, mul, zero, x):
    if n == 1:
        return True
    if x == zero:
        return False
    for y in range(n):
        if y != zero and mul[x][y] == zero:
            return False
    return True

def has_regular(n, mul, zero, S):
    return any(is_regular(n, mul, zero, x) for x in S)

def get_IJ(n, add, mul, I, J):
    products = set()
    for i in I:
        for j in J:
            products.add(mul[i][j])
    
    closure = list(products)
    added = True
    while added:
        added = False
        new_elements = []
        for x in closure:
            for y in closure:
                s = add[x][y]
                if s not in closure and s not in new_elements:
                    new_elements.append(s)
        if new_elements:
            closure.extend(new_elements)
            added = True
            
    added = True
    while added:
        added = False
        new_elements = []
        for x in closure:
            for r in range(n):
                p = mul[x][r]
                if p not in closure and p not in new_elements:
                    new_elements.append(p)
        if new_elements:
            closure.extend(new_elements)
            added = True
            
    return closure

def conditions(witness) -> list[bool]:
    try:
        n = witness.n
        add = witness.add
        mul = witness.mul
        I = witness.I
        J = witness.J
    except AttributeError:
        try:
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            I = witness['I']
            J = witness['J']
        except (TypeError, KeyError):
            return [False, False, False, False, False]
            
    try:
        h1 = is_commutative_ring(n, add, mul)
    except Exception:
        h1 = False
        
    try:
        zero = get_zero(n, add)
        h2 = is_ideal(n, add, mul, zero, I)
    except Exception:
        h2 = False
        
    try:
        zero = get_zero(n, add)
        h3 = has_regular(n, mul, zero, I)
    except Exception:
        h3 = False
        
    try:
        zero = get_zero(n, add)
        h4 = has_regular(n, mul, zero, J)
    except Exception:
        h4 = False
        
    try:
        zero = get_zero(n, add)
        IJ = get_IJ(n, add, mul, I, J)
        neg_q = not has_regular(n, mul, zero, IJ)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: I contains at least one regular element",
    "H_4: J contains at least one regular element",
    "not Q: The product ideal IJ does not contain at least one regular element"
]

N_HYP = 4
NEG_Q_INDEX = 4