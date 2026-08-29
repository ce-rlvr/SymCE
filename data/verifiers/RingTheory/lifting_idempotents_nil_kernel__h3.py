import sympy
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide Z and Zn_Ring for convenience in constructing counterexamples.

class Z_Ring:
    def __init__(self):
        self.name = 'Z'
        
    def add(self, a, b): 
        return a + b
        
    def mul(self, a, b): 
        return a * b
        
    def zero(self): 
        return 0
        
    def one(self): 
        return 1
        
    def contains(self, a): 
        return isinstance(a, (int, sympy.Integer))
        
    def idempotents(self): 
        return [0, 1]
        
    def test_elements(self):
        res = [0]
        for i in range(1, 101):
            res.extend([i, -i])
        return res
        
    def __str__(self): 
        return "Z"

class Zn_Ring:
    def __init__(self, n):
        self.n = int(n)
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def zero(self): 
        return 0
        
    def one(self): 
        return 1
        
    def contains(self, a): 
        return isinstance(a, (int, sympy.Integer)) and 0 <= a < self.n
        
    def idempotents(self):
        return [x for x in range(self.n) if (x * x) % self.n == x]
        
    def test_elements(self): 
        return list(range(self.n))
        
    def __str__(self): 
        return f"Z/{self.n}Z"

Z = Z_Ring()

def conditions(witness):
    try:
        R, S, f, e = witness
    except Exception:
        return [False, False, False, False]
    
    def is_ring(ring):
        try:
            elements = ring.test_elements()
            z = ring.zero()
            o = ring.one()
            if not ring.contains(z) or not ring.contains(o): 
                return False
            
            claimed_idemps = set(ring.idempotents())
            actual_idemps_in_test = set(x for x in elements if ring.mul(x, x) == x)
            if not actual_idemps_in_test.issubset(claimed_idemps): 
                return False
            for x in claimed_idemps:
                if not ring.contains(x) or ring.mul(x, x) != x: 
                    return False
                
            for a in elements:
                has_inv = False
                for b in elements:
                    if ring.add(a, b) == z:
                        has_inv = True
                        break
                if not has_inv: 
                    return False
                
            test_triplets = list(itertools.product(elements[:15], repeat=3))
            for a, b, c in test_triplets:
                if ring.add(a, b) != ring.add(b, a): return False
                if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): return False
                if ring.add(a, z) != a: return False
                
                if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): return False
                if ring.mul(a, o) != a: return False
                if ring.mul(o, a) != a: return False
                
                if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): return False
                if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): return False
            return True
        except Exception:
            return False

    # H_1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H_2: f is a surjective ring homomorphism from R to S
    try:
        elements = R.test_elements()
        images = set()
        h2 = True
        for a in elements:
            fa = f(a)
            if not S.contains(fa): 
                h2 = False
                break
            images.add(fa)
            
        if h2:
            for y in S.test_elements():
                if y not in images:
                    h2 = False
                    break
                    
        if h2:
            test_pairs = list(itertools.product(elements[:30], repeat=2))
            for a, b in test_pairs:
                if f(R.add(a, b)) != S.add(f(a), f(b)):
                    h2 = False
                    break
                if f(R.mul(a, b)) != S.mul(f(a), f(b)):
                    h2 = False
                    break
                    
        if h2 and f(R.one()) != S.one():
            h2 = False
    except Exception:
        h2 = False

    # H_3: e is an idempotent element in S
    try:
        h3 = S.contains(e) and S.mul(e, e) == e
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist an idempotent element E in R such that f(E) = e
    try:
        neg_q = True
        for E in R.idempotents():
            if f(E) == e:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism from R to S",
    "H_3: e is an idempotent element in S",
    "¬Q: There does not exist an idempotent element E in R such that f(E) = e"
]

N_HYP = 3
NEG_Q_INDEX = 3