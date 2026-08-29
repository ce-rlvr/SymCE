import sympy
from sympy.matrices import eye, zeros
from sympy import Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return list(witness[0]), list(witness[1]), list(witness[2]), lambda a, b: a + b, lambda a, b: a * b
        elif len(witness) == 5:
            return list(witness[0]), list(witness[1]), list(witness[2]), witness[3], witness[4]
    elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'I'):
        add = witness.add if hasattr(witness, 'add') else lambda a, b: a + b
        mul = witness.mul if hasattr(witness, 'mul') else lambda a, b: a * b
        return list(witness.R), list(witness.S), list(witness.I), add, mul
    raise ValueError("Invalid witness format")

def find_zero(R, add):
    if not R: 
        return None
    for x in R:
        is_zero = True
        for y in R:
            if add(x, y) != y or add(y, x) != y:
                is_zero = False
                break
        if is_zero:
            return x
    return None

def get_additive_inverse(x, R, add, zero):
    for y in R:
        if add(x, y) == zero and add(y, x) == zero:
            return y
    return None

def generate_ideal(A, R, add, mul, zero):
    J = [zero]
    for a in A:
        if a not in J:
            J.append(a)
            inv = get_additive_inverse(a, R, add, zero)
            if inv is not None and inv not in J:
                J.append(inv)
                
    head = 0
    while head < len(J):
        x = J[head]
        head += 1
        
        n = len(J)
        for i in range(n):
            y = J[i]
            s1 = add(x, y)
            if s1 not in J:
                J.append(s1)
                inv = get_additive_inverse(s1, R, add, zero)
                if inv is not None and inv not in J:
                    J.append(inv)
            s2 = add(y, x)
            if s2 not in J:
                J.append(s2)
                inv = get_additive_inverse(s2, R, add, zero)
                if inv is not None and inv not in J:
                    J.append(inv)
                    
        for r in R:
            p1 = mul(r, x)
            if p1 not in J:
                J.append(p1)
                inv = get_additive_inverse(p1, R, add, zero)
                if inv is not None and inv not in J:
                    J.append(inv)
            p2 = mul(x, r)
            if p2 not in J:
                J.append(p2)
                inv = get_additive_inverse(p2, R, add, zero)
                if inv is not None and inv not in J:
                    J.append(inv)
    return J

def check_H1(R, S, zero, mul):
    if zero in S: 
        return False
    for x in S:
        if x not in R: 
            return False
        for y in S:
            if mul(x, y) not in S:
                return False
    return True

def check_H2(R, S, I, zero, add, mul):
    if zero not in I: 
        return False
    for x in I:
        if x not in R: 
            return False
        inv = get_additive_inverse(x, R, add, zero)
        if inv is None or inv not in I: 
            return False
        for y in I:
            if add(x, y) not in I: 
                return False
        for r in R:
            if mul(r, x) not in I: 
                return False
            if mul(x, r) not in I: 
                return False
            
    for x in I:
        if x in S: 
            return False
        
    for e in R:
        if e not in I:
            J = generate_ideal(list(I) + [e], R, add, mul, zero)
            intersects = any(x in S for x in J)
            if not intersects:
                return False
    return True

def check_Q(R, I, add, mul, zero):
    if len(I) == len(R): 
        return False
    for a in R:
        if a in I: 
            continue
        for b in R:
            if b in I: 
                continue
            Id_a = generate_ideal([a], R, add, mul, zero)
            Id_b = generate_ideal([b], R, add, mul, zero)
            
            subset = True
            for x in Id_a:
                for y in Id_b:
                    if mul(x, y) not in I:
                        subset = False
                        break
                if not subset:
                    break
            if subset:
                return False
    return True

def conditions(witness):
    try:
        R, S, I, add, mul = extract_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        zero = find_zero(R, add)
        if zero is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = check_H1(R, S, zero, mul)
    except Exception:
        h1 = False

    try:
        h2 = check_H2(R, S, I, zero, add, mul)
    except Exception:
        h2 = False

    try:
        q = check_Q(R, I, add, mul, zero)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R not containing 0",
    "H_2: I is an ideal of R that is maximal with respect to the property of being disjoint from S",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2