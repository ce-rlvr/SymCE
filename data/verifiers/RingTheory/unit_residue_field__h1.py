import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def unique_elements(elements, eq):
    unique = []
    for x in elements:
        if not any(eq(x, y) for y in unique):
            unique.append(x)
    return unique

def is_ring(elements, add, mul, eq, is_zero):
    if not elements: return False
    for a in elements:
        for b in elements:
            try:
                c_add = add(a, b)
                if not any(eq(c_add, x) for x in elements): return False
                c_mul = mul(a, b)
                if not any(eq(c_mul, x) for x in elements): return False
            except Exception:
                return False
    has_zero = False
    for a in elements:
        if is_zero(a):
            has_zero = True
            break
    if not has_zero: return False
    for a in elements:
        has_inv = False
        for b in elements:
            if is_zero(add(a, b)):
                has_inv = True
                break
        if not has_inv: return False
    return True

def get_ideal_closure(subset, R, add, mul, eq, is_zero):
    ideal = []
    for x in subset:
        if not any(eq(x, y) for y in ideal):
            ideal.append(x)
    changed = True
    while changed:
        changed = False
        new_elements = []
        for x in ideal:
            for y in ideal:
                z = add(x, y)
                if not any(eq(z, w) for w in ideal + new_elements):
                    new_elements.append(z)
            for y in R:
                if is_zero(add(x, y)):
                    if not any(eq(y, w) for w in ideal + new_elements):
                        new_elements.append(y)
                    break
            for r in R:
                z1 = mul(r, x)
                if not any(eq(z1, w) for w in ideal + new_elements):
                    new_elements.append(z1)
                z2 = mul(x, r)
                if not any(eq(z2, w) for w in ideal + new_elements):
                    new_elements.append(z2)
        if new_elements:
            ideal.extend(new_elements)
            changed = True
    return ideal

def get_all_ideals(R, add, mul, eq, is_zero):
    principal_ideals = []
    for a in R:
        pid = get_ideal_closure([a], R, add, mul, eq, is_zero)
        idx_set = []
        for x in pid:
            for i, r in enumerate(R):
                if eq(x, r):
                    idx_set.append(i)
                    break
        pid_indices = tuple(sorted(idx_set))
        if pid_indices not in principal_ideals:
            principal_ideals.append(pid_indices)
    
    ideals = set(principal_ideals)
    changed = True
    while changed:
        changed = False
        new_ideals = set()
        for i1 in ideals:
            for i2 in ideals:
                sum_ideal_indices = set(i1).union(set(i2))
                subset = [R[i] for i in sum_ideal_indices]
                closure = get_ideal_closure(subset, R, add, mul, eq, is_zero)
                idx_set = []
                for x in closure:
                    for i, r in enumerate(R):
                        if eq(x, r):
                            idx_set.append(i)
                            break
                closure_indices = tuple(sorted(idx_set))
                if closure_indices not in ideals and closure_indices not in new_ideals:
                    new_ideals.add(closure_indices)
        if new_ideals:
            ideals.update(new_ideals)
            changed = True
            
    return [[R[i] for i in idx_tuple] for idx_tuple in ideals]

def is_maximal_ideal(m, R, ideals, eq):
    if len(m) == len(R): return False
    for ideal in ideals:
        if len(ideal) == len(R): continue
        if len(ideal) <= len(m): continue
        is_contained = True
        for x in m:
            if not any(eq(x, y) for y in ideal):
                is_contained = False
                break
        if is_contained:
            return False
    return True

def check_local_ring(R, m, add, mul, eq, is_zero):
    if not is_ring(R, add, mul, eq, is_zero):
        return False
    ideals = get_all_ideals(R, add, mul, eq, is_zero)
    maximal_ideals = []
    for ideal in ideals:
        if is_maximal_ideal(ideal, R, ideals, eq):
            maximal_ideals.append(ideal)
    if len(maximal_ideals) != 1:
        return False
    max_ideal = maximal_ideals[0]
    
    if len(m) != len(max_ideal):
        return False
    for x in m:
        if not any(eq(x, y) for y in max_ideal):
            return False
    for x in max_ideal:
        if not any(eq(x, y) for y in m):
            return False
    return True

def get_identity(R, mul, eq):
    for e in R:
        is_id = True
        for a in R:
            if not eq(mul(e, a), a) or not eq(mul(a, e), a):
                is_id = False
                break
        if is_id:
            return e
    return None

def is_unit(x, R, mul, eq):
    e = get_identity(R, mul, eq)
    if e is None:
        return False
    for y in R:
        if eq(mul(x, y), e) and eq(mul(y, x), e):
            return True
    return False

def image_is_nonzero(x, m, eq):
    for y in m:
        if eq(x, y):
            return False
    return True

def get_ops(witness):
    R = m = x = n = None
    
    if isinstance(witness, tuple):
        if len(witness) == 4 and isinstance(witness[0], int):
            n, R, m, x = witness
        elif len(witness) == 3:
            R, m, x = witness
    elif isinstance(witness, dict):
        R = witness.get('R')
        m = witness.get('m')
        x = witness.get('x')
        n = witness.get('n')
    else:
        try:
            R = witness.R
            m = witness.m
            x = witness.x
            n = getattr(witness, 'n', None)
        except Exception:
            pass

    if R is None or m is None or x is None:
        return None

    if n is not None:
        def add(a, b): return (a + b) % n
        def mul(a, b): return (a * b) % n
        def eq(a, b): 
            try:
                diff = (a - b) % n
                return diff == diff - diff
            except Exception:
                return False
        def is_zero(a): 
            try:
                modded = a % n
                return modded == modded - modded
            except Exception:
                return False
    else:
        def add(a, b): return a + b
        def mul(a, b): return a * b
        def eq(a, b): 
            try:
                diff = a - b
                return diff == diff - diff
            except Exception:
                return False
        def is_zero(a): 
            try:
                return a == a - a
            except Exception:
                return False
                
    return R, m, x, add, mul, eq, is_zero

def conditions(witness):
    try:
        ops = get_ops(witness)
        if ops is None:
            return [False, False, False]
        R, m, x, add, mul, eq, is_zero = ops
        
        R = unique_elements(list(R), eq)
        m = unique_elements(list(m), eq)
        
        try:
            h1 = check_local_ring(R, m, add, mul, eq, is_zero)
        except Exception:
            h1 = False
            
        try:
            h2 = any(eq(x, y) for y in R)
        except Exception:
            h2 = False
            
        try:
            unit_x = is_unit(x, R, mul, eq)
            nonzero_image = image_is_nonzero(x, m, eq)
            q = (unit_x == nonzero_image)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a local ring with maximal ideal m",
    "H_2: x is an element of R",
    "¬Q: x is a unit in R if and only if the image of x in R/m is non-zero is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2