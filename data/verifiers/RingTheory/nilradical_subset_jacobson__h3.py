import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def parse_witness(w):
    if isinstance(w, dict) and 'elements' in w:
        return w['elements'], w.get('add', lambda a, b: a + b), w.get('mul', lambda a, b: a * b), w.get('zero', 0)
    if hasattr(w, 'elements') and hasattr(w, 'add') and hasattr(w, 'mul') and hasattr(w, 'zero'):
        return w.elements, w.add, w.mul, w.zero
    
    elements = list(w)
    add = lambda a, b: a + b
    mul = lambda a, b: a * b
    
    zero = None
    for e in elements:
        is_zero = True
        for el in elements:
            try:
                if not is_eq(add(e, el), el) or not is_eq(add(el, e), el):
                    is_zero = False
                    break
            except Exception:
                is_zero = False
                break
        if is_zero:
            zero = e
            break
            
    return elements, add, mul, zero

def is_commutative_ring(elements, add, mul, zero):
    n = len(elements)
    if n == 0: return False
    if zero not in elements: return False
    
    for i in elements:
        for j in elements:
            if add(i, j) != add(j, i): return False
            
    for i in elements:
        if add(i, zero) != i: return False
        
    for i in elements:
        has_inv = False
        for j in elements:
            if add(i, j) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for i in elements:
        for j in elements:
            for k in elements:
                if add(add(i, j), k) != add(i, add(j, k)): return False
                
    for i in elements:
        for j in elements:
            if mul(i, j) != mul(j, i): return False
            
    for i in elements:
        for j in elements:
            for k in elements:
                if mul(mul(i, j), k) != mul(i, mul(j, k)): return False
                
    for i in elements:
        for j in elements:
            for k in elements:
                if mul(i, add(j, k)) != add(mul(i, j), mul(i, k)): return False
                
    return True

def get_nilradical(elements, mul, zero):
    nilradical = []
    n = len(elements)
    for el in elements:
        p = el
        is_nil = False
        for _ in range(n):
            if p == zero:
                is_nil = True
                break
            p = mul(p, el)
        if is_nil:
            nilradical.append(el)
    return nilradical

def get_all_ideals(elements, add, mul, zero):
    def ideal_gen_by(gens):
        closure = set(gens)
        closure.add(zero)
        changed = True
        while changed:
            changed = False
            new_elements = set()
            for a in closure:
                for b in closure:
                    s = add(a, b)
                    if s not in closure and s not in new_elements:
                        new_elements.add(s)
                for r in elements:
                    p = mul(a, r)
                    if p not in closure and p not in new_elements:
                        new_elements.add(p)
            if new_elements:
                closure.update(new_elements)
                changed = True
        return frozenset(closure)

    zero_ideal = ideal_gen_by([])
    principal_ideals = {ideal_gen_by([el]) for el in elements}
    
    known_ideals = set(principal_ideals)
    known_ideals.add(zero_ideal)
    
    queue = list(known_ideals)
    while queue:
        I = queue.pop(0)
        for pi in principal_ideals:
            sum_ideal = frozenset({add(i, j) for i in I for j in pi})
            if sum_ideal not in known_ideals:
                known_ideals.add(sum_ideal)
                queue.append(sum_ideal)
                
    return known_ideals

def get_maximal_ideals(ideals, R_set):
    proper_ideals = [I for I in ideals if I != R_set]
    maximal_ideals = []
    for I in proper_ideals:
        is_maximal = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_maximal = False
                break
        if is_maximal:
            maximal_ideals.append(I)
    return maximal_ideals

def get_jacobson_radical(maximal_ideals, R_set):
    if not maximal_ideals:
        return R_set
    j_rad = set(maximal_ideals[0])
    for I in maximal_ideals[1:]:
        j_rad = j_rad.intersection(I)
    return j_rad

def conditions(witness):
    try:
        if hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
            h2 = True
            neg_q = not set(witness.nilradical()).issubset(witness.jacobson_radical())
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        raw_elements, raw_add, raw_mul, raw_zero = parse_witness(witness)
        n = len(raw_elements)
        if n == 0:
            return [False, False, False]
            
        zero = -1
        for i, el in enumerate(raw_elements):
            if is_eq(el, raw_zero):
                zero = i
                break
        if zero == -1:
            return [False, False, False]
            
        def get_index(e):
            for i, el in enumerate(raw_elements):
                if is_eq(el, e):
                    return i
            raise ValueError("Element not found")
            
        add_table = [[0]*n for _ in range(n)]
        mul_table = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                add_table[i][j] = get_index(raw_add(raw_elements[i], raw_elements[j]))
                mul_table[i][j] = get_index(raw_mul(raw_elements[i], raw_elements[j]))
                
        elements = list(range(n))
        def add(i, j): return add_table[i][j]
        def mul(i, j): return mul_table[i][j]
        
        h1 = is_commutative_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        if h1:
            nilrad = get_nilradical(elements, mul, zero)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            ideals = get_all_ideals(elements, add, mul, zero)
            R_set = frozenset(elements)
            max_ideals = get_maximal_ideals(ideals, R_set)
            j_rad = get_jacobson_radical(max_ideals, R_set)
            
            neg_q = not set(nilrad).issubset(j_rad)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Nil(R) is the nilradical of R",
    "¬Q: Nil(R) is not contained in J(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2