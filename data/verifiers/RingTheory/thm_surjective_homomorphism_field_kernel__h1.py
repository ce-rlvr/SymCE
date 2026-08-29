import itertools
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_ring(obj, prefix):
    if isinstance(obj, dict):
        if prefix + 'elements' in obj:
            elems = obj[prefix + 'elements']
            add_map = obj[prefix + 'add']
            mul_map = obj[prefix + 'mul']
        elif prefix.strip('_') in obj and isinstance(obj[prefix.strip('_')], dict):
            ring = obj[prefix.strip('_')]
            elems = ring.get('elements')
            add_map = ring.get('add')
            mul_map = ring.get('mul')
        else:
            return None, None, None
            
        if isinstance(add_map, dict):
            add_func = lambda a, b: add_map[(a, b)]
        else:
            add_func = add_map
            
        if isinstance(mul_map, dict):
            mul_func = lambda a, b: mul_map[(a, b)]
        else:
            mul_func = mul_map
            
        return elems, add_func, mul_func
    else:
        ring = getattr(obj, prefix.strip('_'), None)
        if ring:
            elems = getattr(ring, 'elements', None)
            add_func = getattr(ring, 'add', None)
            mul_func = getattr(ring, 'mul', None)
            return elems, add_func, mul_func
    return None, None, None

def is_field(elems, add, mul):
    if not elems or len(elems) < 2: 
        return False
    
    zero = None
    for e in elems:
        if all(add(e, x) == x and add(x, e) == x for x in elems):
            zero = e
            break
    if zero is None: 
        return False
    
    one = None
    for e in elems:
        if all(mul(e, x) == x and mul(x, e) == x for x in elems):
            one = e
            break
    if one is None or one == zero: 
        return False
    
    for a in elems:
        for b in elems:
            if mul(a, b) != mul(b, a): 
                return False
            
    for a in elems:
        if a == zero: 
            continue
        has_inv = False
        for b in elems:
            if mul(a, b) == one:
                has_inv = True
                break
        if not has_inv: 
            return False
            
    return True

def is_surj_hom(R_elems, R_add, R_mul, F_elems, F_add, F_mul, f):
    if isinstance(f, dict):
        f_func = lambda x: f[x]
    else:
        f_func = f
        
    image = []
    for r in R_elems:
        val = f_func(r)
        if val not in image:
            image.append(val)
            
    if len(image) != len(F_elems): 
        return False
    for e in F_elems:
        if e not in image: 
            return False
        
    for a in R_elems:
        for b in R_elems:
            if f_func(R_add(a, b)) != F_add(f_func(a), f_func(b)): 
                return False
            if f_func(R_mul(a, b)) != F_mul(f_func(a), f_func(b)): 
                return False
            
    return True

def kernel_is_maximal(R_elems, R_add, R_mul, F_elems, F_add, F_mul, f):
    if isinstance(f, dict):
        f_func = lambda x: f[x]
    else:
        f_func = f
        
    F_zero = None
    for e in F_elems:
        if all(F_add(e, x) == x for x in F_elems):
            F_zero = e
            break
            
    ker = [r for r in R_elems if f_func(r) == F_zero]
    
    if len(ker) == len(R_elems): 
        return False
    
    is_comm = True
    for a in R_elems:
        for b in R_elems:
            if R_mul(a, b) != R_mul(b, a):
                is_comm = False
                break
        if not is_comm: 
            break
            
    has_id = False
    for e in R_elems:
        if all(R_mul(e, x) == x and R_mul(x, e) == x for x in R_elems):
            has_id = True
            break
            
    if not is_comm or not has_id:
        return False

    def is_ideal(subset):
        for a in subset:
            for b in subset:
                if R_add(a, b) not in subset:
                    return False
        for a in subset:
            for r in R_elems:
                if R_mul(a, r) not in subset:
                    return False
                if R_mul(r, a) not in subset:
                    return False
        return True

    remaining = [x for x in R_elems if x not in ker]
    for i in range(1, len(remaining)):
        for combo in itertools.combinations(remaining, i):
            subset = ker + list(combo)
            if is_ideal(subset):
                return False
                
    return True

def conditions(witness):
    try:
        F_elems, F_add, F_mul = extract_ring(witness, 'F_')
        h1 = is_field(F_elems, F_add, F_mul)
    except Exception:
        h1 = False
        
    try:
        R_elems, R_add, R_mul = extract_ring(witness, 'R_')
        F_elems, F_add, F_mul = extract_ring(witness, 'F_')
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('hom'))
        else:
            f = getattr(witness, 'f', getattr(witness, 'hom', None))
        h2 = is_surj_hom(R_elems, R_add, R_mul, F_elems, F_add, F_mul, f)
    except Exception:
        h2 = False
        
    try:
        R_elems, R_add, R_mul = extract_ring(witness, 'R_')
        F_elems, F_add, F_mul = extract_ring(witness, 'F_')
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('hom'))
        else:
            f = getattr(witness, 'f', getattr(witness, 'hom', None))
        q = kernel_is_maximal(R_elems, R_add, R_mul, F_elems, F_add, F_mul, f)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f: R -> F is a surjective ring homomorphism",
    "¬Q: The kernel of f is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2