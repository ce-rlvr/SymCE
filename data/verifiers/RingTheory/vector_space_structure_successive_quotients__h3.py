import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def make_callable(op, elements):
    if callable(op):
        return op
    elif isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    elif isinstance(op, list):
        elements_list = list(elements)
        return lambda a, b: op[elements_list.index(a)][elements_list.index(b)]
    else:
        raise ValueError("Unsupported operation format")

def get_ring_attributes(witness):
    if isinstance(witness, dict):
        elements = witness['elements']
        add = witness['add']
        mul = witness['mul']
        M = witness['M']
        n = witness.get('n', 1)
    elif isinstance(witness, tuple):
        elements = witness[0]
        add = witness[1]
        mul = witness[2]
        M = witness[3]
        n = witness[4] if len(witness) >= 5 else 1
    else:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        M = witness.M
        n = getattr(witness, 'n', 1)
        
    add_fn = make_callable(add, elements)
    mul_fn = make_callable(mul, elements)
    
    try:
        n = int(n)
    except Exception:
        n = 1
        
    return list(elements), add_fn, mul_fn, list(M), n

def get_zero(elements, add):
    for z in elements:
        if all(add(z, a) == a for a in elements):
            return z
    return None

def is_commutative_ring(elements, add, mul, z):
    if z is None: return False
    
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == z:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            if add(a, b) != add(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    for a in elements:
        for b in elements:
            if mul(a, b) != mul(b, a): return False
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    return True

def is_maximal_ideal(elements, add, mul, M, z):
    if not M: return False
    if z not in M: return False
    
    for a in M:
        has_inv = False
        for b in M:
            if add(a, b) == z:
                has_inv = True
                break
        if not has_inv: return False
        for b in M:
            if add(a, b) not in M: return False
            
    for m in M:
        for r in elements:
            if mul(r, m) not in M: return False
            
    if set(M) == set(elements): return False
    
    for x in elements:
        if x in M: continue
        
        gen_by_x = set()
        Zx = set()
        curr = x
        for _ in range(len(elements) + 1):
            if curr in Zx:
                break
            Zx.add(curr)
            curr = add(curr, x)
        Zx.add(z)
        
        for r in elements:
            rx = mul(r, x)
            for kx in Zx:
                gen_by_x.add(add(rx, kx))
                
        ideal_I = set()
        for m in M:
            for g in gen_by_x:
                ideal_I.add(add(m, g))
                
        if len(ideal_I) != len(elements):
            return False
            
    return True

def compute_ideal_power(elements, add, mul, M, z, n):
    if n <= 0:
        return set(elements)
    if n == 1:
        return set(M)
    
    current_power = set(M)
    for _ in range(n - 1):
        products = set()
        for a in current_power:
            for b in M:
                products.add(mul(a, b))
        
        I = set(products)
        for _ in range(len(elements) + 1):
            new_I = set(I)
            for a in I:
                for b in I:
                    new_I.add(add(a, b))
            for a in I:
                for b in elements:
                    if add(a, b) == z:
                        new_I.add(b)
            if len(new_I) == len(I):
                break
            I = new_I
        current_power = I
        
    return current_power

def is_vector_space(elements, add, mul, M, z, n):
    cosets = []
    for r in elements:
        coset = frozenset(add(r, m) for m in M)
        if coset not in cosets:
            cosets.append(coset)
            
    zero_coset = frozenset(M)
    
    def mul_coset(c1, c2):
        a = next(iter(c1))
        b = next(iter(c2))
        ab = mul(a, b)
        return frozenset(add(ab, m) for m in M)
        
    id_coset = None
    for e in cosets:
        if all(mul_coset(e, c) == c for c in cosets):
            id_coset = e
            break
            
    if id_coset is None or id_coset == zero_coset:
        return False
        
    for c in cosets:
        if c == zero_coset: continue
        has_inv = False
        for d in cosets:
            if mul_coset(c, d) == id_coset:
                has_inv = True
                break
        if not has_inv:
            return False
            
    Mn = compute_ideal_power(elements, add, mul, M, z, n)
    Mn_plus_1 = compute_ideal_power(elements, add, mul, M, z, n + 1)
    
    if len(Mn_plus_1) == 0:
        return False
        
    if len(Mn) % len(Mn_plus_1) != 0:
        return False
    dim_size = len(Mn) // len(Mn_plus_1)
    
    field_size = len(cosets)
    
    if dim_size > 1:
        temp = dim_size
        while temp % field_size == 0:
            temp = temp // field_size
        if temp != 1:
            return False
            
    e = next(iter(id_coset))
    for x in Mn:
        ex = mul(e, x)
        neg_x = None
        for b in elements:
            if add(x, b) == z:
                neg_x = b
                break
        if neg_x is None:
            return False
        diff = add(ex, neg_x)
        if diff not in Mn_plus_1:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, M, n = get_ring_attributes(witness)
        z = get_zero(elements, add)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(elements, add, mul, z)
    except Exception:
        h1 = False
        
    try:
        h2 = is_maximal_ideal(elements, add, mul, M, z)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_vector_space(elements, add, mul, M, z, n)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a maximal ideal of R",
    "¬Q: The quotient module M^n / M^{n+1} is not a vector space over the field R/M"
]

N_HYP = 2
NEG_Q_INDEX = 2