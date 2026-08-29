import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def get_ring_ops(witness):
    if isinstance(witness, dict):
        elements = witness.get('elements')
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        S = witness.get('S')
    else:
        elements = getattr(witness, 'elements', None)
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        zero = getattr(witness, 'zero', None)
        S = getattr(witness, 'S', None)
        
    if elements is None or add is None or mul is None or zero is None or S is None:
        return None, None, None, None, None
        
    elements = list(elements)
    S = list(S)
    
    if isinstance(add, list):
        add_fn = lambda a, b: add[elements.index(a)][elements.index(b)]
    elif isinstance(add, dict):
        add_fn = lambda a, b: add[(a, b)]
    else:
        add_fn = add
        
    if isinstance(mul, list):
        mul_fn = lambda a, b: mul[elements.index(a)][elements.index(b)]
    elif isinstance(mul, dict):
        mul_fn = lambda a, b: mul[(a, b)]
    else:
        mul_fn = mul
        
    return elements, add_fn, mul_fn, zero, S

def check_H1(elements, add_fn, mul_fn, zero):
    try:
        n = len(elements)
        if n == 0: return False
        if zero not in elements: return False
        
        for a in elements:
            if add_fn(a, zero) != a or add_fn(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add_fn(a, b) == zero and add_fn(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                ab_add = add_fn(a, b)
                if ab_add not in elements: return False
                if ab_add != add_fn(b, a): return False
                
                ab_mul = mul_fn(a, b)
                if ab_mul not in elements: return False
                if ab_mul != mul_fn(b, a): return False
                
                for c in elements:
                    if add_fn(ab_add, c) != add_fn(a, add_fn(b, c)): return False
                    if mul_fn(ab_mul, c) != mul_fn(a, mul_fn(b, c)): return False
                    
                    if mul_fn(a, add_fn(b, c)) != add_fn(ab_mul, mul_fn(a, c)): return False
        return True
    except Exception:
        return False

def check_H2(elements, mul_fn, S):
    try:
        if not S:
            return False
        for s in S:
            if s not in elements:
                return False
        for s1 in S:
            for s2 in S:
                if mul_fn(s1, s2) not in S:
                    return False
        return True
    except Exception:
        return False

def get_nilradical(elements, mul_fn, zero):
    N = []
    for e in elements:
        curr = e
        is_nil = False
        for _ in range(len(elements)):
            if curr == zero:
                is_nil = True
                break
            curr = mul_fn(curr, e)
            if curr is None:
                break
        if is_nil:
            N.append(e)
    return N

def get_localized_ring(elements, add_fn, mul_fn, zero, S):
    if not S:
        return None
        
    mul_cache = {}
    for a in elements:
        for b in elements:
            mul_cache[(a, b)] = mul_fn(a, b)
            
    def fast_mul(a, b):
        return mul_cache.get((a, b))

    pairs = [(r, s) for r in elements for s in S]
    
    def is_eq(p1, p2):
        r1, s1 = p1
        r2, s2 = p2
        m1 = fast_mul(r1, s2)
        m2 = fast_mul(r2, s1)
        if m1 is None or m2 is None:
            return False
        for u in S:
            if fast_mul(u, m1) == fast_mul(u, m2):
                return True
        return False

    classes = []
    for p in pairs:
        found = False
        for c in classes:
            if is_eq(p, c[0]):
                c.append(p)
                found = True
                break
        if not found:
            classes.append([p])
            
    loc_elements = list(range(len(classes)))
    
    loc_zero = None
    for i, c in enumerate(classes):
        if is_eq(c[0], (zero, S[0])):
            loc_zero = i
            break
            
    def loc_mul(i, j):
        r1, s1 = classes[i][0]
        r2, s2 = classes[j][0]
        prod = (fast_mul(r1, r2), fast_mul(s1, s2))
        for k, c in enumerate(classes):
            if is_eq(prod, c[0]):
                return k
        return None
        
    return loc_elements, loc_mul, loc_zero, classes

def check_neg_Q(elements, add_fn, mul_fn, zero, S):
    try:
        N = get_nilradical(elements, mul_fn, zero)
        
        loc_ring = get_localized_ring(elements, add_fn, mul_fn, zero, S)
        if loc_ring is None:
            return False
        loc_elements, loc_mul, loc_zero, classes = loc_ring
        
        loc_N = get_nilradical(loc_elements, loc_mul, loc_zero)
        
        S_inv_N = []
        for i, c in enumerate(classes):
            is_in_S_inv_N = False
            for (r, s) in c:
                if r in N:
                    is_in_S_inv_N = True
                    break
            if is_in_S_inv_N:
                S_inv_N.append(i)
                
        return set(loc_N) != set(S_inv_N)
    except Exception:
        return False

def conditions(witness):
    try:
        elements, add_fn, mul_fn, zero, S = get_ring_ops(witness)
        if elements is None:
            return [False, False, False]
            
        h1 = check_H1(elements, add_fn, mul_fn, zero)
        h2 = check_H2(elements, mul_fn, S)
        neg_q = check_neg_Q(elements, add_fn, mul_fn, zero, S)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The nilradical of the localization S^{-1}R is NOT equal to S^{-1}N"
]

N_HYP = 2
NEG_Q_INDEX = 2