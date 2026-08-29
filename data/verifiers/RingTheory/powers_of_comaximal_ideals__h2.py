import itertools
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, item):
    return any(e == item for e in lst)

def sets_equal(A, B):
    for a in A:
        if not contains(B, a): return False
    for b in B:
        if not contains(A, b): return False
    return True

def set_add(A, B, add):
    res = []
    for a in A:
        for b in B:
            s = add(a, b)
            if not contains(res, s):
                res.append(s)
    return res

def product_set(A, m, mul):
    if m == 1:
        return list(A)
    current = list(A)
    for _ in range(m - 1):
        next_set = []
        for a in current:
            for b in A:
                val = mul(a, b)
                if not contains(next_set, val):
                    next_set.append(val)
        current = next_set
    return current

def additive_closure(S, add):
    closure = []
    for item in S:
        if not contains(closure, item):
            closure.append(item)
    
    queue = list(closure)
    while queue:
        curr = queue.pop(0)
        new_elements = []
        for y in closure:
            z1 = add(curr, y)
            if not contains(closure, z1) and not contains(new_elements, z1):
                new_elements.append(z1)
            z2 = add(y, curr)
            if not contains(closure, z2) and not contains(new_elements, z2):
                new_elements.append(z2)
        for z in new_elements:
            closure.append(z)
            queue.append(z)
    return closure

def is_ideal(I, R, add, mul):
    if not I: return False
    # Check closure under addition
    for a in I:
        for b in I:
            if not contains(I, add(a, b)): return False
    # Check absorption
    for a in I:
        for r in R:
            if not contains(I, mul(a, r)): return False
            if not contains(I, mul(r, a)): return False
            
    # Check for additive inverses
    zeros_list = [z for z in R if all(add(z, a) == a for a in R)]
    if not zeros_list: return False
    zero = zeros_list[0]
    
    for a in I:
        if not any(add(a, b) == zero for b in I): return False
        
    return True

def is_commutative_ring(R, add, mul):
    if not R: return False
    # Check closure and commutativity
    for a in R:
        for b in R:
            if not contains(R, add(a, b)): return False
            if not contains(R, mul(a, b)): return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            
    # Check associativity and distributivity
    for a in R:
        for b in R:
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    # Check identity for addition
    zeros_list = [z for z in R if all(add(z, a) == a for a in R)]
    if not zeros_list: return False
    zero = zeros_list[0]
    
    # Check additive inverses
    for a in R:
        if not any(add(a, b) == zero for b in R): return False
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['ring']
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
            I = witness['I']
            J = witness['J']
            m = witness['m']
            n = witness['n']
        elif len(witness) == 7:
            R, add, mul, I, J, m, n = witness
        else:
            R, I, J, m, n = witness
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = is_commutative_ring(R, add, mul)
    except Exception:
        h1 = False

    # H_2: I + J = R (and they are ideals)
    try:
        I_plus_J = set_add(I, J, add)
        h2 = sets_equal(I_plus_J, R) and is_ideal(I, R, add, mul) and is_ideal(J, R, add, mul)
    except Exception:
        h2 = False

    # H_3: m and n are positive integers
    try:
        h3 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h3 = False

    # ¬Q: I^m + J^n != R
    try:
        Im_gens = product_set(I, m, mul)
        Im = additive_closure(Im_gens, add)
        
        Jn_gens = product_set(J, n, mul)
        Jn = additive_closure(Jn_gens, add)
        
        Im_plus_Jn = set_add(Im, Jn, add)
        
        neg_q = not sets_equal(Im_plus_Jn, R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I + J = R",
    "H_3: m and n are positive integers",
    "¬Q: I^m + J^n != R"
]

N_HYP = 3
NEG_Q_INDEX = 3