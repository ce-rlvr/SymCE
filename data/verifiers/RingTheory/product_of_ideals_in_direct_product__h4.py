import itertools

def is_ring(elems, add, mul, zero):
    if zero not in elems:
        return False
    # Check additive group
    for a in elems:
        if add(a, zero) != a or add(zero, a) != a:
            return False
        has_inv = False
        for b in elems:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv:
            return False
            
    for a in elems:
        for b in elems:
            sum_ab = add(a, b)
            mul_ab = mul(a, b)
            if sum_ab not in elems or mul_ab not in elems:
                return False
            if sum_ab != add(b, a):
                return False
            for c in elems:
                if add(sum_ab, c) != add(a, add(b, c)):
                    return False
                if mul(mul_ab, c) != mul(a, mul(b, c)):
                    return False
                if mul(a, add(b, c)) != add(mul_ab, mul(a, c)):
                    return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                    return False
    return True

def is_ideal(elems, add, mul, zero, I):
    if not I:
        return False
    I_set = set(I)
    if zero not in I_set:
        return False
    if not I_set.issubset(set(elems)):
        return False
    for a in I_set:
        for b in I_set:
            if add(a, b) not in I_set:
                return False
        has_inv = False
        for b in I_set:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv:
            return False
        for r in elems:
            if mul(r, a) not in I_set:
                return False
            if mul(a, r) not in I_set:
                return False
    return True

def additive_closure(S, add):
    closure = set(S)
    added = True
    while added:
        added = False
        new_elems = set()
        for a in closure:
            for b in closure:
                c = add(a, b)
                if c not in closure and c not in new_elems:
                    new_elems.add(c)
                    added = True
        if new_elems:
            closure.update(new_elems)
    return closure

def subset_product(A, B, add, mul):
    pairwise = set()
    for a in A:
        for b in B:
            pairwise.add(mul(a, b))
    if not pairwise:
        return set()
    return additive_closure(pairwise, add)

def conditions(witness):
    try:
        R1_elems = list(witness['R1_elems'])
        R1_add = witness['R1_add']
        R1_mul = witness['R1_mul']
        R1_zero = witness['R1_zero']
        
        R2_elems = list(witness['R2_elems'])
        R2_add = witness['R2_add']
        R2_mul = witness['R2_mul']
        R2_zero = witness['R2_zero']
        
        I1 = list(witness['I1'])
        J1 = list(witness['J1'])
        I2 = list(witness['I2'])
        J2 = list(witness['J2'])
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_ring(R1_elems, R1_add, R1_mul, R1_zero) and is_ring(R2_elems, R2_add, R2_mul, R2_zero)
    except Exception:
        h1 = False
        
    h2 = True
    
    try:
        h3 = is_ideal(R1_elems, R1_add, R1_mul, R1_zero, I1) and is_ideal(R1_elems, R1_add, R1_mul, R1_zero, J1)
    except Exception:
        h3 = False
        
    try:
        if not set(I2).issubset(set(R2_elems)) or not set(J2).issubset(set(R2_elems)):
            neg_q = False
        else:
            def R_add(x, y):
                return (R1_add(x[0], y[0]), R2_add(x[1], y[1]))
                
            def R_mul(x, y):
                return (R1_mul(x[0], y[0]), R2_mul(x[1], y[1]))
                
            I1xI2 = list(itertools.product(I1, I2))
            J1xJ2 = list(itertools.product(J1, J2))
            
            LHS = subset_product(I1xI2, J1xJ2, R_add, R_mul)
            
            I1J1 = subset_product(I1, J1, R1_add, R1_mul)
            I2J2 = subset_product(I2, J2, R2_add, R2_mul)
            RHS = set(itertools.product(I1J1, I2J2))
            
            neg_q = (set(LHS) != set(RHS))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: R is the direct product ring R_1 x R_2",
    "H_3: I_1 and J_1 are ideals of R_1",
    "¬Q: (I_1 x I_2)(J_1 x J_2) != (I_1 J_1) x (I_2 J_2)"
]

N_HYP = 3
NEG_Q_INDEX = 3