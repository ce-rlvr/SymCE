import itertools

class MatrixRing:
    """
    Represents the ring of n x n matrices over Z/pZ.
    """
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.elements = self._generate_elements()
        self.zero = tuple([0] * (n * n))
        
        one = [0] * (n * n)
        for i in range(n):
            one[i * n + i] = 1
        self.one = tuple(one)
        
    def _generate_elements(self):
        return list(itertools.product(range(self.p), repeat=self.n * self.n))
        
    def add(self, A, B):
        return tuple((a + b) % self.p for a, b in zip(A, B))
        
    def mul(self, A, B):
        n = self.n
        p = self.p
        C = [0] * (n * n)
        for i in range(n):
            for j in range(n):
                s = 0
                for k in range(n):
                    s += A[i * n + k] * B[k * n + j]
                C[i * n + j] = s % p
        return tuple(C)

class ZMod:
    """
    Represents the ring Z/nZ.
    """
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n

def is_ring(R):
    """
    Verifies that R is a valid finite ring (and thus Artinian).
    Checks ring axioms exhaustively. Limited to 256 elements to ensure fast execution.
    """
    try:
        elements = list(R.elements)
        n = len(elements)
        if n == 0 or n > 256:
            return False
        zero = R.zero
        one = R.one
        if zero not in elements or one not in elements:
            return False
        
        for a in elements:
            if R.add(a, zero) != a or R.add(zero, a) != a: return False
            if R.mul(a, one) != a or R.mul(one, a) != a: return False
            
            has_neg = False
            for b in elements:
                if R.add(a, b) == zero and R.add(b, a) == zero:
                    has_neg = True
                    break
            if not has_neg: return False
            
            for b in elements:
                ab = R.add(a, b)
                if ab not in elements: return False
                m_ab = R.mul(a, b)
                if m_ab not in elements: return False
                if ab != R.add(b, a): return False
                
                for c in elements:
                    if R.add(ab, c) != R.add(a, R.add(b, c)): return False
                    if R.mul(m_ab, c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(m_ab, R.mul(a, c)): return False
                    if R.mul(ab, c) != R.add(R.mul(a, c), R.mul(b, c)): return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: R is an Artinian ring
    # Any finite ring is Artinian. We verify it's a valid finite ring.
    h1 = is_ring(witness)
    
    # neg_Q: R is NOT isomorphic to a finite direct product of Artinian local rings
    # A finite ring is a direct product of local rings iff every idempotent is central.
    # Therefore, it is NOT a direct product of local rings iff there exists a non-central idempotent.
    try:
        elements = list(witness.elements)
        has_non_central_idempotent = False
        for e in elements:
            if witness.mul(e, e) == e:
                is_central = True
                for x in elements:
                    if witness.mul(e, x) != witness.mul(x, e):
                        is_central = False
                        break
                if not is_central:
                    has_non_central_idempotent = True
                    break
        neg_q = has_non_central_idempotent
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of Artinian local rings"
]

N_HYP = 1
NEG_Q_INDEX = 1