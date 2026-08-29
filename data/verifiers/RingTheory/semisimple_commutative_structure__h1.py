import itertools
from sympy import Matrix, eye, zeros

# --- Top-level setup: named object bindings ---

class ModRingElement:
    """A matrix ring element over Z/nZ."""
    def __init__(self, mat, n):
        self.mat = mat
        self.n = n
        
    def __add__(self, other):
        return ModRingElement((self.mat + other.mat).applyfunc(lambda x: x % self.n), self.n)
        
    def __mul__(self, other):
        return ModRingElement((self.mat * other.mat).applyfunc(lambda x: x % self.n), self.n)
        
    def __sub__(self, other):
        return ModRingElement((self.mat - other.mat).applyfunc(lambda x: x % self.n), self.n)
        
    def __eq__(self, other):
        if not isinstance(other, ModRingElement): 
            return False
        return self.mat == other.mat and self.n == other.n
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        return hash((tuple(self.mat), self.n))
        
    def __repr__(self):
        return f"ModRingElement({self.mat}, {self.n})"

class ZMod:
    """An element of Z/nZ."""
    def __init__(self, val, n):
        self.val = val % n
        self.n = n
        
    def __add__(self, other):
        return ZMod((self.val + other.val) % self.n, self.n)
        
    def __mul__(self, other):
        return ZMod((self.val * other.val) % self.n, self.n)
        
    def __sub__(self, other):
        return ZMod((self.val - other.val) % self.n, self.n)
        
    def __eq__(self, other):
        if not isinstance(other, ZMod): 
            return False
        return self.val == other.val and self.n == other.n
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        return hash((self.val, self.n))
        
    def __repr__(self):
        return f"ZMod({self.val}, {self.n})"

# Pre-defined finite rings for the witness expression to reference
M2_F2 = [ModRingElement(Matrix([[a, b], [c, d]]), 2) for a, b, c, d in itertools.product([0, 1], repeat=4)]
M2_F3 = [ModRingElement(Matrix([[a, b], [c, d]]), 3) for a, b, c, d in itertools.product([0, 1, 2], repeat=4)]

Z2 = [ZMod(i, 2) for i in range(2)]
Z3 = [ZMod(i, 3) for i in range(3)]
Z4 = [ZMod(i, 4) for i in range(4)]
Z6 = [ZMod(i, 6) for i in range(6)]

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# --- Verifier logic ---

def conditions(witness) -> list[bool]:
    try:
        # We expect the witness to be a finite collection of elements forming a ring
        if not isinstance(witness, (list, tuple, set)):
            return [False, False, False]
        
        R = list(witness)
        n = len(R)
        
        # Limit size to prevent timeouts (M2_F2 has 16 elements, M2_F3 has 81)
        if n == 0 or n > 100:
            return [False, False, False]
            
        # Find the additive identity (zero)
        zero = None
        for x in R:
            if x + x == x:
                zero = x
                break
        if zero is None:
            return [False, False, False]
            
        # Check ring axioms (closure and additive inverses)
        is_ring = True
        for x in R:
            has_inv = False
            for y in R:
                if x + y == zero:
                    has_inv = True
                    break
            if not has_inv:
                is_ring = False
                break
                
            for y in R:
                if (x + y) not in R:
                    is_ring = False
                    break
                if (x * y) not in R:
                    is_ring = False
                    break
            if not is_ring:
                break
                
        if not is_ring:
            return [False, False, False]
            
        # H_1: R is an Artinian ring
        # Any finite ring is Artinian.
        h1 = True
        
        # H_2: The Jacobson radical of R is the zero ideal
        # J(R) = { x in R | for all y in R, xy is right quasi-regular }
        # w is right quasi-regular iff there exists z in R such that w + z - wz = 0
        J = []
        for x in R:
            is_in_J = True
            for y in R:
                xy = x * y
                is_rqr = False
                for z in R:
                    if xy + z - xy * z == zero:
                        is_rqr = True
                        break
                if not is_rqr:
                    is_in_J = False
                    break
            if is_in_J:
                J.append(x)
                
        h2 = (len(J) == 1 and J[0] == zero)
        
        # ¬Q: R is NOT isomorphic to a finite direct product of fields
        # By the Artin-Wedderburn theorem, a finite Artinian ring with J(R)=0 
        # is a finite direct product of fields IF AND ONLY IF it is commutative.
        # Thus, the conclusion fails iff the ring is NOT commutative.
        is_comm = True
        for x in R:
            for y in R:
                if x * y != y * x:
                    is_comm = False
                    break
            if not is_comm:
                break
                
        neg_q = not is_comm
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "H_2: The Jacobson radical of R is the zero ideal",
    "¬Q: R is not isomorphic to a finite direct product of fields"
]

N_HYP = 2
NEG_Q_INDEX = 2