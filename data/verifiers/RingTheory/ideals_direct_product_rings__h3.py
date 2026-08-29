import itertools
import math

class ZnRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def __eq__(self, other): 
        return isinstance(other, ZnRing) and self.n == other.n
        
    def __hash__(self): 
        return hash(self.n)

# Pre-defined common finite rings for convenience
Z2 = ZnRing(2)
Z3 = ZnRing(3)
Z4 = ZnRing(4)
Z5 = ZnRing(5)
Z6 = ZnRing(6)

def get_ring(R):
    if isinstance(R, int):
        if R < 1: 
            raise ValueError("Ring size must be >= 1")
        return ZnRing(R)
    return R

def is_ring_with_identity(R):
    try:
        elements = R.elements
        if len(elements) > 100: 
            return False
        zero = R.zero
        one = R.one
        if zero not in elements or one not in elements: 
            return False
        
        for a in elements:
            if R.add(a, zero) != a or R.add(zero, a) != a: 
                return False
            if R.mul(a, one) != a or R.mul(one, a) != a: 
                return False
            
        for a in elements:
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero and R.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: 
                return False
            
        for a in elements:
            for b in elements:
                if R.add(a, b) != R.add(b, a): 
                    return False
                
        for a in elements:
            for b in elements:
                ab_add = R.add(a, b)
                ab_mul = R.mul(a, b)
                if ab_add not in elements: 
                    return False
                if ab_mul not in elements: 
                    return False
                for c in elements:
                    if R.add(ab_add, c) != R.add(a, R.add(b, c)): 
                        return False
                    if R.mul(ab_mul, c) != R.mul(a, R.mul(b, c)): 
                        return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): 
                        return False
                    if R.mul(ab_add, c) != R.add(R.mul(a, c), R.mul(b, c)): 
                        return False
        return True
    except Exception:
        return False

def is_ideal(J, R):
    if not J: 
        return False
    for x in J:
        if x not in R.elements: 
            return False
    if R.zero not in J: 
        return False
    for x in J:
        has_inv = False
        for y in J:
            if R.add(x, y) == R.zero and R.add(y, x) == R.zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        for y in J:
            if R.add(x, y) not in J: 
                return False
    for x in J:
        for r in R.elements:
            if R.mul(r, x) not in J: 
                return False
            if R.mul(x, r) not in J: 
                return False
    return True

def conditions(witness):
    """
    witness should be a tuple: (R1, R2, I)
    where R1 and R2 are rings (or integers n representing Z_n),
    and I is a list/iterable of pairs (x, y) representing a subset of R1 x R2.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R1_raw, R2_raw, I_raw = witness
        I = list(I_raw)
    except Exception:
        return [False, False, False]
        
    # H_1: Let R1 and R2 be rings with identity.
    try:
        R1 = get_ring(R1_raw)
        R2 = get_ring(R2_raw)
        h1 = is_ring_with_identity(R1) and is_ring_with_identity(R2)
    except Exception:
        h1 = False

    # H_2: Let R = R1 x R2 be the direct product of R1 and R2.
    # We verify this by checking if I is a well-formed subset of R1 x R2.
    try:
        h2 = False
        if h1:
            is_subset = True
            for item in I:
                if not isinstance(item, (tuple, list)) or len(item) != 2:
                    is_subset = False
                    break
                x, y = item
                if x not in R1.elements or y not in R2.elements:
                    is_subset = False
                    break
            h2 = is_subset
    except Exception:
        h2 = False

    # ¬Q: I is NOT uniquely the product of two-sided ideals I1 and I2.
    try:
        neg_q = False
        if h1 and h2:
            I_set = set(tuple(item) for item in I)
            I1 = set(x for x, y in I_set)
            I2 = set(y for x, y in I_set)
            
            is_prod_of_ideals = True
            if not is_ideal(I1, R1):
                is_prod_of_ideals = False
            elif not is_ideal(I2, R2):
                is_prod_of_ideals = False
            else:
                expected_I = set((x, y) for x in I1 for y in I2)
                if I_set != expected_I:
                    is_prod_of_ideals = False
                    
            neg_q = not is_prod_of_ideals
        elif h1 and not h2:
            # If I is not even a subset of R1 x R2, it cannot be a product of ideals
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings with identity",
    "H_2: R is the direct product of R1 and R2",
    "¬Q: I is not uniquely the product of two-sided ideals I1 and I2"
]

N_HYP = 2
NEG_Q_INDEX = 2