import sympy
import itertools

# Top-level setup
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def parse_witness(witness):
    if witness == sympy.ZZ or witness == sympy.QQ:
        return witness
        
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        witness = int(witness)
        
    if isinstance(witness, int):
        if witness <= 1 or witness > 500:
            return None
        n = witness
        add = [[(i + j) % n for j in range(n)] for i in range(n)]
        mul = [[(i * j) % n for j in range(n)] for i in range(n)]
        return n, add, mul
        
    if isinstance(witness, (list, tuple)):
        if len(witness) == 0:
            return None
        parsed = []
        for val in witness:
            if hasattr(val, 'is_Integer') and val.is_Integer:
                parsed.append(int(val))
            elif isinstance(val, int):
                parsed.append(val)
            else:
                return None
        for n in parsed:
            if n <= 1:
                return None
                
        # Check size before generating all elements to prevent timeouts
        size = 1
        for n in parsed:
            size *= n
        if size > 500:
            return None
            
        elements = list(itertools.product(*(range(n) for n in parsed)))
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        add = [[0] * size for _ in range(size)]
        mul = [[0] * size for _ in range(size)]
        
        # Ensure index 0 is the zero element
        zero_elem = tuple(0 for _ in parsed)
        z_idx = elem_to_idx[zero_elem]
        elements[0], elements[z_idx] = elements[z_idx], elements[0]
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        for i, e1 in enumerate(elements):
            for j, e2 in enumerate(elements):
                sum_e = tuple((a + b) % n for a, b, n in zip(e1, e2, parsed))
                prod_e = tuple((a * b) % n for a, b, n in zip(e1, e2, parsed))
                add[i][j] = elem_to_idx[sum_e]
                mul[i][j] = elem_to_idx[prod_e]
                
        return size, add, mul
        
    return None

def compute_minimal_euclidean_function(size, add, mul):
    d = {0: -1}
    R_k = {0}
    current_k = 0
    
    while len(R_k) < size:
        new_R_k = set(R_k)
        for b in range(1, size):
            if b in R_k:
                continue
            
            multiples = set(mul[b][q] for q in range(size))
            covered = set()
            for m in multiples:
                for r in R_k:
                    covered.add(add[m][r])
                    
            if len(covered) == size:
                new_R_k.add(b)
                d[b] = current_k
                
        if len(new_R_k) == len(R_k):
            return None
            
        R_k = new_R_k
        current_k += 1
        
    return d

def conditions(witness):
    try:
        ring = parse_witness(witness)
    except Exception:
        return [False, False]
        
    if ring is None:
        return [False, False]
        
    if ring == sympy.ZZ or ring == sympy.QQ:
        # Both are Euclidean domains, so they admit a Euclidean function.
        # They are integral domains, so they DO admit a submultiplicative one.
        return [True, False]
        
    size, add, mul = ring
    
    try:
        d = compute_minimal_euclidean_function(size, add, mul)
        h1 = (d is not None)
    except Exception:
        h1 = False
        
    try:
        # The condition "d(a) <= d(ab) for all non-zero a, b" requires d(ab) to be defined.
        # Since d is a Euclidean function, its domain is R \ {0}.
        # If there are zero divisors, ab = 0 for some non-zero a, b, making d(ab) undefined.
        # Thus, the condition fails universally for any ring with zero divisors.
        # Conversely, every finite Euclidean integral domain (finite field) trivially satisfies it.
        has_zero_divisors = False
        for a in range(1, size):
            for b in range(1, size):
                if mul[a][b] == 0:
                    has_zero_divisors = True
                    break
            if has_zero_divisors:
                break
        neg_q = has_zero_divisors
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R admits a Euclidean function",
    "¬Q: R does not admit a Euclidean function d such that d(a) <= d(ab) for all non-zero a, b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1