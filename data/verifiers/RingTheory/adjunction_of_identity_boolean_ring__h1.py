import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We define standard cyclic rings as integers, which our get_ring_ops will interpret as Z_n.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def get_ring_ops(witness):
    """
    Extracts the elements, addition function, multiplication function, and zero element
    from the witness. Supports integers (for Z_n), tuples, dicts, or objects.
    """
    if isinstance(witness, int):
        n = witness
        if n <= 0:
            raise ValueError("Ring size must be positive")
        return list(range(n)), lambda x, y: (x + y) % n, lambda x, y: (x * y) % n, 0
    elif isinstance(witness, tuple) and len(witness) == 4:
        return witness
    elif isinstance(witness, dict):
        return witness['elements'], witness['add'], witness['mul'], witness['zero']
    else:
        return witness.elements, witness.add, witness.mul, witness.zero

def is_ring(elements, add, mul, zero):
    """
    Verifies that the given structure is a valid ring.
    """
    if not isinstance(elements, (list, tuple, set)):
        return False
    elements = list(elements)
    if len(elements) > 50:
        return False  # Limit size to ensure fast verification
    if zero not in elements:
        return False
        
    for a in elements:
        # Identity for addition
        if add(a, zero) != a or add(zero, a) != a: 
            return False
            
        # Inverse for addition
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
            
        for b in elements:
            # Closure
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            
            # Commutativity of addition
            if add(a, b) != add(b, a): return False
            
            for c in elements:
                # Associativity of addition
                if add(add(a, b), c) != add(a, add(b, c)): return False
                # Associativity of multiplication
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                # Distributivity
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    return True

def check_conclusion(elements, add, mul, zero):
    """
    Checks if R' is a Boolean ring with identity (0, 1) and contains a subring isomorphic to R.
    """
    def mul_int(a, n):
        # n is in Z_2, so it's either 0 or 1
        return a if n == 1 else zero
    
    R_prime = [(a, m) for a in elements for m in (0, 1)]
    
    def add_prime(x, y):
        return (add(x[0], y[0]), (x[1] + y[1]) % 2)
        
    def mul_prime(x, y):
        term1 = mul(x[0], y[0])
        term2 = mul_int(x[0], y[1])
        term3 = mul_int(y[0], x[1])
        return (add(add(term1, term2), term3), (x[1] * y[1]) % 2)
        
    # Check if R' is a Boolean ring (x^2 = x for all x)
    is_boolean = True
    for x in R_prime:
        if mul_prime(x, x) != x:
            is_boolean = False
            break
            
    # Check if (0, 1) is the identity
    has_identity = True
    id_elem = (zero, 1)
    for x in R_prime:
        if mul_prime(x, id_elem) != x or mul_prime(id_elem, x) != x:
            has_identity = False
            break
            
    # The subset {(a, 0) | a in R} is always a subring isomorphic to R by construction.
    has_subring = True 
    
    return is_boolean and has_identity and has_subring

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    try:
        elements, add, mul, zero = get_ring_ops(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        # The conclusion holds if R' is a Boolean ring with identity (0,1) and has a subring isomorphic to R.
        # We want neg_q to be True when the conclusion FAILS.
        q_holds = check_conclusion(elements, add, mul, zero)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: R' is not a Boolean ring with identity (0,1) or lacks a subring isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1