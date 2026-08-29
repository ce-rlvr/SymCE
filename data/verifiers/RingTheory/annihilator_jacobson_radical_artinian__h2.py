import sympy
from sympy import eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The left annihilator of J(R) in R is not a non-zero two-sided ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_ring_ops(witness):
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        elements = list(witness.elements)
        add = witness.add
        mul = witness.mul
        eq = getattr(witness, 'eq', lambda x, y: x == y)
    elif isinstance(witness, (list, tuple, set)):
        elements = list(witness)
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        eq = lambda x, y: x == y
    else:
        elements = [witness]
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        eq = lambda x, y: x == y
        
    zero = None
    for z in elements:
        if all(eq(add(z, x), x) and eq(add(x, z), x) for x in elements):
            zero = z
            break
    if zero is None:
        raise ValueError("No zero element found")

    def neg(x):
        for y in elements:
            if eq(add(x, y), zero) and eq(add(y, x), zero):
                return y
        raise ValueError("No additive inverse")

    return elements, add, mul, zero, eq, neg

def is_ring(elements, add, mul, eq, zero, neg):
    if not elements:
        return False
    for a in elements:
        for b in elements:
            s = add(a, b)
            if not any(eq(s, x) for x in elements): return False
            
    for a in elements:
        for b in elements:
            if not eq(add(a, b), add(b, a)): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                
    for a in elements:
        if not eq(add(a, zero), a): return False
        
    for a in elements:
        if not eq(add(a, neg(a)), zero): return False
        
    for a in elements:
        for b in elements:
            p = mul(a, b)
            if not any(eq(p, x) for x in elements): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                
    for a in elements:
        for b in elements:
            for c in elements:
                if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
                
    return True

def ideal_generated_by(x, elements, add, mul, eq, zero, neg):
    ideal = [x]
    if not any(eq(zero, i) for i in ideal):
        ideal.append(zero)
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in ideal:
            na = neg(a)
            if not any(eq(na, i) for i in ideal + new_elements):
                new_elements.append(na)
            for b in ideal:
                s = add(a, b)
                if not any(eq(s, i) for i in ideal + new_elements):
                    new_elements.append(s)
            for r in elements:
                p1 = mul(r, a)
                if not any(eq(p1, i) for i in ideal + new_elements):
                    new_elements.append(p1)
                p2 = mul(a, r)
                if not any(eq(p2, i) for i in ideal + new_elements):
                    new_elements.append(p2)
        if new_elements:
            ideal.extend(new_elements)
            changed = True
            if len(ideal) > len(elements) * 2:
                break
    return ideal

def multiply_ideals(I1, I2, elements, add, mul, eq, zero, neg):
    products = []
    for a in I1:
        for b in I2:
            p = mul(a, b)
            if not any(eq(p, x) for x in products):
                products.append(p)
    
    closure = list(products)
    if not any(eq(zero, x) for x in closure):
        closure.append(zero)
        
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in closure:
            na = neg(a)
            if not any(eq(na, x) for x in closure + new_elements):
                new_elements.append(na)
            for b in closure:
                s = add(a, b)
                if not any(eq(s, x) for x in closure + new_elements):
                    new_elements.append(s)
        if new_elements:
            closure.extend(new_elements)
            changed = True
    return closure

def is_nilpotent_ideal(I, elements, add, mul, eq, zero, neg):
    if all(eq(x, zero) for x in I):
        return True
    current_power = list(I)
    for _ in range(len(elements) + 1):
        current_power = multiply_ideals(current_power, I, elements, add, mul, eq, zero, neg)
        if all(eq(x, zero) for x in current_power):
            return True
    return False

def get_J_R(elements, add, mul, eq, zero, neg):
    J = []
    for x in elements:
        Ix = ideal_generated_by(x, elements, add, mul, eq, zero, neg)
        if is_nilpotent_ideal(Ix, elements, add, mul, eq, zero, neg):
            J.append(x)
    return J

def get_left_annihilator(J, elements, mul, eq, zero):
    L = []
    for r in elements:
        if all(eq(mul(r, j), zero) for j in J):
            L.append(r)
    return L

def is_two_sided_ideal(L, elements, add, mul, eq, zero, neg):
    if not L:
        return False
    for a in L:
        if not any(eq(neg(a), x) for x in L):
            return False
        for b in L:
            if not any(eq(add(a, b), x) for x in L):
                return False
    for a in L:
        for r in elements:
            if not any(eq(mul(r, a), x) for x in L):
                return False
            if not any(eq(mul(a, r), x) for x in L):
                return False
    return True

def conditions(witness):
    try:
        elements, add, mul, zero, eq, neg = get_ring_ops(witness)
        h1 = is_ring(elements, add, mul, eq, zero, neg)
    except Exception:
        h1 = False

    try:
        elements, add, mul, zero, eq, neg = get_ring_ops(witness)
        if not is_ring(elements, add, mul, eq, zero, neg):
            neg_q = False
        else:
            J = get_J_R(elements, add, mul, eq, zero, neg)
            L = get_left_annihilator(J, elements, mul, eq, zero)
            
            is_non_zero = any(not eq(x, zero) for x in L)
            is_ideal = is_two_sided_ideal(L, elements, add, mul, eq, zero, neg)
            
            q = is_non_zero and is_ideal
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]