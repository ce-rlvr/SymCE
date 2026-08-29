import itertools

class ZnRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def __eq__(self, other): 
        return isinstance(other, ZnRing) and self.n == other.n
        
    def __hash__(self): 
        return hash(('ZnRing', self.n))
        
    def __str__(self): 
        return f"ZnRing({self.n})"
        
    def __repr__(self): 
        return str(self)

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elements = list(itertools.product(R1.elements, R2.elements))
        self.zero = (R1.zero, R2.zero)
        self.one = (R1.one, R2.one)
        
    def add(self, a, b): 
        return (self.R1.add(a[0], b[0]), self.R2.add(a[1], b[1]))
        
    def mul(self, a, b): 
        return (self.R1.mul(a[0], b[0]), self.R2.mul(a[1], b[1]))
        
    def __str__(self): 
        return f"ProductRing({self.R1}, {self.R2})"
        
    def __repr__(self): 
        return str(self)

def is_ideal(ring, subset):
    if not subset: 
        return False
    subset_set = set(subset)
    if ring.zero not in subset_set: 
        return False
        
    for a in subset_set:
        for b in subset_set:
            if ring.add(a, b) not in subset_set: 
                return False
                
    for r in ring.elements:
        for a in subset_set:
            if ring.mul(r, a) not in subset_set: 
                return False
            if ring.mul(a, r) not in subset_set: 
                return False
                
    return True

def is_primary_ideal(ring, subset):
    if not is_ideal(ring, subset): 
        return False
    subset_set = set(subset)
    if len(subset_set) == len(ring.elements): 
        return False 
    
    for a in ring.elements:
        for b in ring.elements:
            if ring.mul(a, b) in subset_set:
                if a in subset_set:
                    continue
                
                b_pow = b
                found = False
                for _ in range(len(ring.elements)):
                    if b_pow in subset_set:
                        found = True
                        break
                    b_pow = ring.mul(b_pow, b)
                    
                if not found:
                    return False
    return True

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        f = witness['f']
        Q = witness['Q']
        
        if not isinstance(R.elements, list) or not isinstance(S.elements, list):
            return [False, False, False]
            
        is_hom = True
        if f(R.one) != S.one: 
            is_hom = False
        for a in R.elements:
            for b in R.elements:
                if f(R.add(a, b)) != S.add(f(a), f(b)): 
                    is_hom = False
                if f(R.mul(a, b)) != S.mul(f(a), f(b)): 
                    is_hom = False
        if not is_hom:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ideal(R, Q)
    except Exception:
        h1 = False
        
    try:
        ker_f = [x for x in R.elements if f(x) == S.zero]
        h2 = all(x in Q for x in ker_f)
    except Exception:
        h2 = False
        
    try:
        q_primary = is_primary_ideal(R, Q)
        f_Q = [f(x) for x in Q]
        fq_primary = is_primary_ideal(S, f_Q)
        
        neg_q = (q_primary != fq_primary)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an ideal of R",
    "H_2: The kernel of f is contained in Q",
    "¬Q: Q is primary in R XOR f(Q) is primary in S"
]

N_HYP = 2
NEG_Q_INDEX = 2