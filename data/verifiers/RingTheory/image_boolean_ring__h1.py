import itertools

class Zn:
    def __init__(self, n):
        self.n = n
        self.elems = list(range(n))
        self.zero = 0
        self.one = 1 % n
    def add(self, x, y): return (x + y) % self.n
    def mul(self, x, y): return (x * y) % self.n

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elems = list(itertools.product(R1.elems, R2.elems))
        self.zero = (R1.zero, R2.zero)
        self.one = (R1.one, R2.one)
    def add(self, x, y):
        return (self.R1.add(x[0], y[0]), self.R2.add(x[1], y[1]))
    def mul(self, x, y):
        return (self.R1.mul(x[0], y[0]), self.R2.mul(x[1], y[1]))

Z2 = Zn(2)
Z3 = Zn(3)
Z4 = Zn(4)
Z5 = Zn(5)
Z6 = Zn(6)
Z8 = Zn(8)
Z9 = Zn(9)
Z10 = Zn(10)
Z12 = Zn(12)

def check_ring(S):
    try:
        elems = S.elems
        zero = S.zero
        one = S.one
        add = S.add
        mul = S.mul
        
        if zero not in elems or one not in elems:
            return False
            
        for a in elems:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            
            has_inv = False
            for b in elems:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elems:
                ab_add = add(a, b)
                if ab_add not in elems: return False
                if ab_add != add(b, a): return False
                
                ab_mul = mul(a, b)
                if ab_mul not in elems: return False
                
                for c in elems:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def check_homomorphism(R, S, f):
    try:
        if not check_ring(R):
            return False
            
        if callable(f):
            f_func = f
        else:
            f_func = lambda x: f[x]
            
        if f_func(R.one) != S.one: 
            return False
        
        for a in R.elems:
            fa = f_func(a)
            if fa not in S.elems: 
                return False
            for b in R.elems:
                fb = f_func(b)
                if f_func(R.add(a, b)) != S.add(fa, fb): return False
                if f_func(R.mul(a, b)) != S.mul(fa, fb): return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        S = witness.get('S')
        R = witness.get('R')
        f = witness.get('f')
    except Exception:
        return [False, False, False]
        
    # H1: S is a ring
    try:
        h1 = check_ring(S)
    except Exception:
        h1 = False
        
    # H2: f is a ring homomorphism from R to S
    try:
        h2 = check_homomorphism(R, S, f)
    except Exception:
        h2 = False
        
    # neg_Q: The image of R under f is NOT a Boolean subring of S
    try:
        if callable(f):
            f_func = f
        else:
            f_func = lambda x: f[x]
            
        image = set(f_func(a) for a in R.elems)
        
        is_boolean = True
        for y in image:
            if S.mul(y, y) != y:
                is_boolean = False
                break
                
        neg_q = not is_boolean
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a ring",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: The image of R under f is not a Boolean subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2