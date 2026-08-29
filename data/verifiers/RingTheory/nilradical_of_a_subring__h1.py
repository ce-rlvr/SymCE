import itertools
from sympy import Matrix, eye, zeros

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ModMatrix:
    """A helper class for matrices over Z/nZ to facilitate finite ring creation."""
    def __init__(self, mat, mod):
        self.mat = mat
        self.mod = mod
        
    def __add__(self, other):
        return ModMatrix((self.mat + other.mat).applyfunc(lambda x: x % self.mod), self.mod)
        
    def __sub__(self, other):
        return ModMatrix((self.mat - other.mat).applyfunc(lambda x: x % self.mod), self.mod)
        
    def __mul__(self, other):
        return ModMatrix((self.mat * other.mat).applyfunc(lambda x: x % self.mod), self.mod)
        
    def __eq__(self, other):
        if not isinstance(other, ModMatrix):
            return False
        return self.mod == other.mod and self.mat == other.mat
        
    def __hash__(self):
        return hash((tuple(self.mat), self.mod))
        
    def __repr__(self):
        return f"ModMatrix({self.mat}, {self.mod})"

def MatrixRing(n, mod):
    """Generates the full matrix ring M_n(Z/mod Z)."""
    elements = []
    for entries in itertools.product(range(mod), repeat=n*n):
        mat = Matrix(n, n, entries)
        elements.append(ModMatrix(mat, mod))
    return elements

def UpperTriangularMatrixRing(n, mod):
    """Generates the upper triangular matrix ring over Z/mod Z."""
    elements = []
    for entries in itertools.product(range(mod), repeat=n*(n+1)//2):
        mat = Matrix(n, n, [0]*(n*n))
        idx = 0
        for i in range(n):
            for j in range(i, n):
                mat[i, j] = entries[idx]
                idx += 1
        elements.append(ModMatrix(mat, mod))
    return elements

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
        R = list(R)
        S = list(S)
        
        if not R or not S:
            return [False, False]
            
        # Find the zero element in S
        zero_S = None
        for z in S:
            if all(z + x == x for x in S):
                zero_S = z
                break
        if zero_S is None:
            return [False, False]
            
        # Find the zero element in R
        zero_R = None
        for z in R:
            if all(z + x == x for x in R):
                zero_R = z
                break
        if zero_R is None or zero_R != zero_S:
            return [False, False]
            
        zero = zero_S
        
        def in_list(a, lst):
            return any(a == x for x in lst)
            
        # H_1: R is a subring of S
        h1 = True
        if not all(in_list(x, S) for x in R):
            h1 = False
        else:
            for a in R:
                for b in R:
                    if not in_list(a - b, R):
                        h1 = False
                        break
                    if not in_list(a * b, R):
                        h1 = False
                        break
                if not h1:
                    break
                    
        def is_nilpotent(x, ring, zero):
            curr = x
            for _ in range(len(ring)):
                if curr == zero:
                    return True
                curr = curr * x
            return False

        def get_nilradical(ring, zero):
            """
            For a finite ring, the prime radical (nilradical) is the largest nilpotent ideal.
            An element x is in the nilradical iff x is nilpotent and both xy and yx are 
            nilpotent for all y in the ring.
            """
            nil = []
            for x in ring:
                if not is_nilpotent(x, ring, zero):
                    continue
                if all(is_nilpotent(x * y, ring, zero) for y in ring):
                    if all(is_nilpotent(y * x, ring, zero) for y in ring):
                        nil.append(x)
            return nil

        nil_S = get_nilradical(S, zero)
        nil_R = get_nilradical(R, zero)
        
        r_cap_nil_S = [x for x in R if in_list(x, nil_S)]
        
        # Check if Nil(R) == R \cap Nil(S)
        subset1 = all(in_list(x, r_cap_nil_S) for x in nil_R)
        subset2 = all(in_list(x, nil_R) for x in r_cap_nil_S)
        
        # neg_Q is True when the conclusion FAILS (i.e., they are NOT equal)
        neg_q = not (subset1 and subset2)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "¬Q: Nil(R) != R ∩ Nil(S)"
]

N_HYP = 1
NEG_Q_INDEX = 1