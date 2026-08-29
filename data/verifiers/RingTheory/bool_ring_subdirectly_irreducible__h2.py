import itertools

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

Z2 = FiniteRing(
    [0, 1], 
    lambda x, y: (x + y) % 2, 
    lambda x, y: (x * y) % 2, 
    0
)

Z2xZ2 = FiniteRing(
    [(0,0), (0,1), (1,0), (1,1)],
    lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2),
    lambda x, y: ((x[0]*y[0])%2, (x[1]*y[1])%2),
    (0,0)
)

Z2xZ2xZ2 = FiniteRing(
    [(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)],
    lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2, (x[2]+y[2])%2),
    lambda x, y: ((x[0]*y[0])%2, (x[1]*y[1])%2, (x[2]*y[2])%2),
    (0,0,0)
)

trivial_ring = FiniteRing(
    [0], 
    lambda x, y: 0, 
    lambda x, y: 0, 
    0
)

def is_ring(R):
    try:
        elements = R.elements
        zero = R.zero
        add = R.add
        mul = R.mul
        
        if zero not in elements: 
            return False
        
        # Closure
        for x in elements:
            for y in elements:
                if add(x, y) not in elements: return False
                if mul(x, y) not in elements: return False
                
        # Additive identity
        for x in elements:
            if add(x, zero) != x or add(zero, x) != x: return False
            
        # Associativity
        for x in elements:
            for y in elements:
                for z in elements:
                    if add(add(x, y), z) != add(x, add(y, z)): return False
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                    
        # Commutativity of addition
        for x in elements:
            for y in elements:
                if add(x, y) != add(y, x): return False
                
        # Additive inverses
        for x in elements:
            has_inv = False
            for y in elements:
                if add(x, y) == zero and add(y, x) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Multiplicative identity (1)
        has_one = False
        for e in elements:
            is_one = True
            for x in elements:
                if mul(e, x) != x or mul(x, e) != x:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
            
        # Distributivity
        for x in elements:
            for y in elements:
                for z in elements:
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                    if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
                    
        return True
    except Exception:
        return False

def is_boolean_ring(R):
    if not is_ring(R): 
        return False
    try:
        for x in R.elements:
            if R.mul(x, x) != x: 
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        h1 = is_boolean_ring(witness)
    except Exception:
        h1 = False
        
    try:
        # Z/2Z has exactly 2 elements. Any Boolean ring of size 2 is isomorphic to Z/2Z.
        # Thus, a finite Boolean ring is NOT isomorphic to Z/2Z iff its size is not 2.
        neg_q = len(witness.elements) != 2
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1