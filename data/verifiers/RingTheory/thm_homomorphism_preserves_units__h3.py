import itertools

class Zn:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
        
    def add(self, x, y):
        return (x + y) % self.n
        
    def mul(self, x, y):
        return (x * y) % self.n
        
    def __repr__(self):
        return f"Zn({self.n})"

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elements = list(itertools.product(R1.elements, R2.elements))
        self.zero = (R1.zero, R2.zero)
        self.one = (R1.one, R2.one)
        
    def add(self, x, y):
        return (self.R1.add(x[0], y[0]), self.R2.add(x[1], y[1]))
        
    def mul(self, x, y):
        return (self.R1.mul(x[0], y[0]), self.R2.mul(x[1], y[1]))
        
    def __repr__(self):
        return f"ProductRing({self.R1}, {self.R2})"

class MatrixRing:
    def __init__(self, n, base_ring):
        self.n = n
        self.base_ring = base_ring
        self.elements = []
        for entries in itertools.product(base_ring.elements, repeat=n*n):
            self.elements.append(tuple(entries))
        self.zero = tuple([base_ring.zero] * (n*n))
        one = []
        for i in range(n):
            for j in range(n):
                one.append(base_ring.one if i == j else base_ring.zero)
        self.one = tuple(one)
        
    def add(self, x, y):
        return tuple(self.base_ring.add(a, b) for a, b in zip(x, y))
        
    def mul(self, x, y):
        n = self.n
        res = []
        for i in range(n):
            for j in range(n):
                val = self.base_ring.zero
                for k in range(n):
                    val = self.base_ring.add(val, self.base_ring.mul(x[i*n+k], y[k*n+j]))
                res.append(val)
        return tuple(res)
        
    def __repr__(self):
        return f"MatrixRing({self.n}, {self.base_ring})"

Z2 = Zn(2)
Z3 = Zn(3)
Z4 = Zn(4)
Z6 = Zn(6)

def apply_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def is_ring_with_identity(R):
    try:
        elements = R.elements
        zero = R.zero
        one = R.one
        if zero not in elements or one not in elements: 
            return False
        
        for x in elements:
            if R.add(x, zero) != x or R.add(zero, x) != x: 
                return False
            
        for x in elements:
            if R.mul(x, one) != x or R.mul(one, x) != x: 
                return False
            
        for x in elements:
            has_neg = False
            for y in elements:
                if R.add(x, y) == zero and R.add(y, x) == zero:
                    has_neg = True
                    break
            if not has_neg: 
                return False
            for y in elements:
                if R.add(x, y) != R.add(y, x): 
                    return False
                for z in elements:
                    if R.add(R.add(x, y), z) != R.add(x, R.add(y, z)): 
                        return False
                    
        for x in elements:
            for y in elements:
                for z in elements:
                    if R.mul(R.mul(x, y), z) != R.mul(x, R.mul(y, z)): 
                        return False
                    if R.mul(x, R.add(y, z)) != R.add(R.mul(x, y), R.mul(x, z)): 
                        return False
                    if R.mul(R.add(x, y), z) != R.add(R.mul(x, z), R.mul(y, z)): 
                        return False
        return True
    except Exception:
        return False

def is_ring_homomorphism(f, R, S):
    try:
        for x in R.elements:
            fx = apply_f(f, x)
            if fx not in S.elements: 
                return False
            for y in R.elements:
                fy = apply_f(f, y)
                if apply_f(f, R.add(x, y)) != S.add(fx, fy): 
                    return False
                if apply_f(f, R.mul(x, y)) != S.mul(fx, fy): 
                    return False
        return True
    except Exception:
        return False

def is_unit(R, u):
    try:
        if u not in R.elements: 
            return False
        for x in R.elements:
            if R.mul(u, x) == R.one and R.mul(x, u) == R.one:
                return True
        return False
    except Exception:
        return False

def get_inv(R, u):
    for x in R.elements:
        if R.mul(u, x) == R.one and R.mul(x, u) == R.one:
            return x
    return None

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        S = witness['S']
        f = witness['f']
        u = witness['u']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_ring_with_identity(R) and is_ring_with_identity(S)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring_homomorphism(f, R, S)
    except Exception:
        h2 = False
        
    try:
        h3 = is_unit(R, u)
    except Exception:
        h3 = False
        
    try:
        fu = apply_f(f, u)
        if not is_unit(S, fu):
            neg_q = True
        else:
            u_inv = get_inv(R, u)
            if u_inv is None:
                neg_q = False
            else:
                fu_inv = get_inv(S, fu)
                if apply_f(f, u_inv) != fu_inv:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R \\to S is a ring homomorphism",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S or f(u^{-1}) != f(u)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3