import itertools

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = elements
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero = zero
        
    def add(self, x, y): 
        return self.add_func(x, y)
        
    def mul(self, x, y): 
        return self.mul_func(x, y)

def make_Z_n(n):
    return FiniteRing(list(range(n)), lambda x, y: (x+y)%n, lambda x, y: (x*y)%n, 0)

Z2 = make_Z_n(2)
Z3 = make_Z_n(3)
Z4 = make_Z_n(4)
Z5 = make_Z_n(5)
Z6 = make_Z_n(6)
Z8 = make_Z_n(8)

# Counterexample: 2Z / 8Z (a commutative ring without identity)
R_2Z8Z = FiniteRing([0, 2, 4, 6], lambda x, y: (x+y)%8, lambda x, y: (x*y)%8, 0)

def extract_ring(witness):
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        zero = witness.zero
        if callable(zero):
            zero = zero()
        return witness.elements, witness.add, witness.mul, zero
    if isinstance(witness, tuple) and len(witness) >= 4:
        if callable(witness[1]) and callable(witness[2]):
            return witness[0], witness[1], witness[2], witness[3]
    raise ValueError("Cannot extract ring structure")

def is_commutative_ring(elements, add, mul, zero):
    n = len(elements)
    if n == 0: 
        return False
        
    for x in elements:
        for y in elements:
            s = add(x, y)
            if s not in elements: return False
            if add(y, x) != s: return False
            p = mul(x, y)
            if p not in elements: return False
            if mul(y, x) != p: return False
            
    for x in elements:
        if add(x, zero) != x: return False
        
    for x in elements:
        has_inv = False
        for y in elements:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    subset = elements if n <= 50 else elements[:10]
    for x in subset:
        for y in subset:
            for z in subset:
                if add(x, add(y, z)) != add(add(x, y), z): return False
                if mul(x, mul(y, z)) != mul(mul(x, y), z): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                
    return True

def get_all_ideals(elements, add, mul, zero):
    def generate_ideal(generators):
        ideal = set(generators)
        ideal.add(zero)
        queue = list(ideal)
        
        while queue:
            x = queue.pop(0)
            for y in list(ideal):
                s = add(x, y)
                if s not in ideal:
                    ideal.add(s)
                    queue.append(s)
                neg_y = None
                for z in elements:
                    if add(y, z) == zero:
                        neg_y = z
                        break
                if neg_y is not None:
                    d = add(x, neg_y)
                    if d not in ideal:
                        ideal.add(d)
                        queue.append(d)
            for r in elements:
                p = mul(r, x)
                if p not in ideal:
                    ideal.add(p)
                    queue.append(p)
        return frozenset(ideal)

    principal_ideals = set()
    for x in elements:
        principal_ideals.add(generate_ideal([x]))
        
    all_ideals = set(principal_ideals)
    queue = list(principal_ideals)
    
    while queue:
        I1 = queue.pop(0)
        for I2 in list(all_ideals):
            sum_ideal = generate_ideal(list(I1) + list(I2))
            if sum_ideal not in all_ideals:
                all_ideals.add(sum_ideal)
                queue.append(sum_ideal)
                
    return all_ideals

def get_maximal_ideals(elements, all_ideals):
    proper_ideals = [I for I in all_ideals if len(I) < len(elements)]
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

def get_jacobson_radical(elements, maximal_ideals):
    if not maximal_ideals:
        return set(elements)
    j_rad = set(maximal_ideals[0])
    for I in maximal_ideals[1:]:
        j_rad = j_rad.intersection(I)
    return j_rad

def get_nilradical(elements, mul, zero):
    nil_set = []
    n = len(elements)
    for x in elements:
        curr = x
        is_nil = False
        for _ in range(n):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, x)
        if is_nil:
            nil_set.append(x)
    return nil_set

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R = witness[0]
        provided_J = witness[1]
    else:
        R = witness
        provided_J = None

    try:
        elements, add, mul, zero = extract_ring(R)
        h1 = is_commutative_ring(elements, add, mul, zero)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
            neg_q = False
        else:
            all_ideals = get_all_ideals(elements, add, mul, zero)
            max_ideals = get_maximal_ideals(elements, all_ideals)
            J_R = get_jacobson_radical(elements, max_ideals)
            
            if provided_J is not None:
                if callable(provided_J):
                    h2 = all((x in J_R) == provided_J(x) for x in elements)
                else:
                    h2 = (set(provided_J) == J_R)
            else:
                h2 = True
                
            Nil_R = get_nilradical(elements, mul, zero)
            
            is_subset = set(Nil_R).issubset(J_R)
            neg_q = not is_subset
    except Exception:
        h2 = False
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J(R) is the Jacobson radical of R",
    "¬Q: Nil(R) is not contained in J(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2