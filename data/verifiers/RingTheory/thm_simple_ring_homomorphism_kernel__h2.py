import sympy as sp
import itertools

class ZRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def zero(self):
        return 0
    def one(self):
        return 1
    def __repr__(self):
        return f"ZRing({self.n})"

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elements = [(a, b) for a in R1.elements for b in R2.elements]
    def add(self, x, y):
        return (self.R1.add(x[0], y[0]), self.R2.add(x[1], y[1]))
    def mul(self, x, y):
        return (self.R1.mul(x[0], y[0]), self.R2.mul(x[1], y[1]))
    def zero(self):
        return (self.R1.zero(), self.R2.zero())
    def one(self):
        return (self.R1.one(), self.R2.one())
    def __repr__(self):
        return f"ProductRing({self.R1}, {self.R2})"

class MatrixRing:
    def __init__(self, n, base_ring):
        self.n = n
        self.base_ring = base_ring
        self.elements = []
        for entries in itertools.product(base_ring.elements, repeat=n*n):
            self.elements.append(tuple(entries))
            
    def add(self, A, B):
        return tuple(self.base_ring.add(a, b) for a, b in zip(A, B))
        
    def mul(self, A, B):
        n = self.n
        C = [self.base_ring.zero()] * (n * n)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i*n + j] = self.base_ring.add(
                        C[i*n + j], 
                        self.base_ring.mul(A[i*n + k], B[k*n + j])
                    )
        return tuple(C)
        
    def zero(self):
        return tuple([self.base_ring.zero()] * (self.n * self.n))
        
    def one(self):
        n = self.n
        I = [self.base_ring.zero()] * (n * n)
        for i in range(n):
            I[i*n + i] = self.base_ring.one()
        return tuple(I)
    def __repr__(self):
        return f"MatrixRing({self.n}, {self.base_ring})"

Z2 = ZRing(2)
Z3 = ZRing(3)
Z4 = ZRing(4)
Z5 = ZRing(5)
Z6 = ZRing(6)
Z8 = ZRing(8)
Z10 = ZRing(10)
Z12 = ZRing(12)

def conditions(witness):
    try:
        R, S, mapping = witness
    except Exception:
        return [False, False, False]
        
    def is_ring(ring):
        try:
            elems = ring.elements
            z = ring.zero()
            if z not in elems: return False
            for a in elems:
                if ring.add(a, z) != a or ring.add(z, a) != a: return False
            for a in elems:
                for b in elems:
                    if ring.add(a, b) != ring.add(b, a): return False
                    for c in elems:
                        if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): return False
                        if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): return False
                        if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): return False
                        if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): return False
            for a in elems:
                has_inv = False
                for b in elems:
                    if ring.add(a, b) == z:
                        has_inv = True
                        break
                if not has_inv: return False
            if hasattr(ring, 'one'):
                one = ring.one()
                if one not in elems: return False
                for a in elems:
                    if ring.mul(a, one) != a or ring.mul(one, a) != a: return False
            return True
        except Exception:
            return False

    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    def is_homomorphism(R, S, mapping):
        try:
            for a in R.elements:
                try:
                    ma = mapping[a] if isinstance(mapping, dict) else mapping(a)
                except Exception:
                    return False
                if ma not in S.elements: return False
                for b in R.elements:
                    mb = mapping[b] if isinstance(mapping, dict) else mapping(b)
                    m_add = mapping[R.add(a, b)] if isinstance(mapping, dict) else mapping(R.add(a, b))
                    m_mul = mapping[R.mul(a, b)] if isinstance(mapping, dict) else mapping(R.mul(a, b))
                    if m_add != S.add(ma, mb): return False
                    if m_mul != S.mul(ma, mb): return False
            if hasattr(R, 'one') and hasattr(S, 'one'):
                m_one = mapping[R.one()] if isinstance(mapping, dict) else mapping(R.one())
                if m_one != S.one(): return False
            return True
        except Exception:
            return False

    try:
        h2 = is_homomorphism(R, S, mapping)
    except Exception:
        h2 = False

    def neg_q_check(R, S, mapping):
        try:
            is_inj = True
            for a in R.elements:
                ma = mapping[a] if isinstance(mapping, dict) else mapping(a)
                for b in R.elements:
                    if a != b:
                        mb = mapping[b] if isinstance(mapping, dict) else mapping(b)
                        if ma == mb:
                            is_inj = False
                            break
                if not is_inj: break
                
            is_zero = True
            z_S = S.zero()
            for a in R.elements:
                ma = mapping[a] if isinstance(mapping, dict) else mapping(a)
                if ma != z_S:
                    is_zero = False
                    break
                    
            return (not is_inj) and (not is_zero)
        except Exception:
            return False

    try:
        neg_q = neg_q_check(R, S, mapping)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: f is neither injective nor the zero homomorphism"
]
N_HYP = 2
NEG_Q_INDEX = 2