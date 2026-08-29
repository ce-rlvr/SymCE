import itertools

class Ring:
    def __init__(self, elements, add_func, mul_func):
        self.elements = list(elements)
        self.add_func = add_func
        self.mul_func = mul_func
        
    def add(self, a, b):
        return self.add_func(a, b)
        
    def mul(self, a, b):
        return self.mul_func(a, b)

def make_Zn(n):
    return Ring(list(range(n)), lambda a, b: (a + b) % n, lambda a, b: (a * b) % n)

# Standard rings with identity
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)

# A valid ring without a multiplicative identity (2Z mod 4Z)
Z2_zero_mul = Ring([0, 2], lambda a, b: (a + b) % 4, lambda a, b: (a * b) % 4)

def is_ring(R):
    if not hasattr(R, 'elements') or not hasattr(R, 'add') or not hasattr(R, 'mul'):
        return False
    elements = R.elements
    if not elements:
        return False
    
    # Check addition closure
    for a in elements:
        for b in elements:
            try:
                c = R.add(a, b)
                if c not in elements: return False
            except Exception:
                return False
                
    # Check addition commutativity
    for a in elements:
        for b in elements:
            if R.add(a, b) != R.add(b, a): return False
            
    # Check addition associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                
    # Check addition identity
    zero = None
    for e in elements:
        if all(R.add(e, a) == a for a in elements):
            zero = e
            break
    if zero is None: return False
    
    # Check addition inverse
    for a in elements:
        if not any(R.add(a, b) == zero for b in elements): return False
        
    # Check multiplication closure
    for a in elements:
        for b in elements:
            try:
                c = R.mul(a, b)
                if c not in elements: return False
            except Exception:
                return False
                
    # Check multiplication associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                
    # Check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
                
    return True

def get_mult_identity(R):
    elements = R.elements
    for e in elements:
        if all(R.mul(e, a) == a and R.mul(a, e) == a for a in elements):
            return e
    return None

def conditions(witness):
    """
    witness should be a tuple (R1, R2) representing the two rings.
    """
    try:
        R1 = witness[0]
        R2 = witness[1]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R1) and get_mult_identity(R1) is not None
    except Exception:
        h1 = False
        
    try:
        # The hypothesis states R1 x R2 is the direct product ring of R1 and R2.
        # This implies R2 must be a valid ring.
        h2 = is_ring(R2)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # The conclusion is that U(R1 x R2) is isomorphic to U(R1) x U(R2).
            # If R2 has no multiplicative identity, then R1 x R2 has no multiplicative identity.
            # In this case, the group of units U(R1 x R2) is undefined (not a group),
            # and U(R2) is undefined, so the isomorphism statement fails.
            # If both have identities, U(R1 x R2) is always isomorphic to U(R1) x U(R2).
            id2 = get_mult_identity(R2)
            if id2 is None:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R1 is a ring with multiplicative identity",
    "H_2: R1 x R2 is the direct product ring of R1 and R2",
    "¬Q: The group of units U(R1 x R2) is not isomorphic to U(R1) x U(R2) (e.g. because one is not a group)"
]

N_HYP = 2
NEG_Q_INDEX = 2