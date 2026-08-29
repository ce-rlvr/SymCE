import sympy
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import sympy.abc as abc
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide ZMod and MatrixMod to easily construct finite rings and matrix rings over Z_n.

class ZMod:
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
    def __add__(self, other):
        return ZMod(self.val + other.val, self.mod)
    def __sub__(self, other):
        return ZMod(self.val - other.val, self.mod)
    def __mul__(self, other):
        return ZMod(self.val * other.val, self.mod)
    def __eq__(self, other):
        return isinstance(other, ZMod) and self.val == other.val and self.mod == other.mod
    def __hash__(self):
        return hash((self.val, self.mod))
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

class MatrixMod:
    def __init__(self, mat, mod):
        self.mat = tuple(tuple(x % mod for x in row) for row in mat)
        self.mod = mod
        self.n = len(mat)
    def __add__(self, other):
        res = tuple(tuple((self.mat[i][j] + other.mat[i][j]) % self.mod for j in range(self.n)) for i in range(self.n))
        return MatrixMod(res, self.mod)
    def __sub__(self, other):
        res = tuple(tuple((self.mat[i][j] - other.mat[i][j]) % self.mod for j in range(self.n)) for i in range(self.n))
        return MatrixMod(res, self.mod)
    def __mul__(self, other):
        res = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                s = sum(self.mat[i][k] * other.mat[k][j] for k in range(self.n)) % self.mod
                row.append(s)
            res.append(tuple(row))
        return MatrixMod(tuple(res), self.mod)
    def __eq__(self, other):
        return isinstance(other, MatrixMod) and self.mat == other.mat and self.mod == other.mod
    def __hash__(self):
        return hash((self.mat, self.mod))
    def __repr__(self):
        return f"MatrixMod({self.mat}, {self.mod})"

# Pre-define some common finite rings
Z2_ring = [ZMod(i, 2) for i in range(2)]
Z3_ring = [ZMod(i, 3) for i in range(3)]
M2_Z2_ring = [MatrixMod(((a,b),(c,d)), 2) for a,b,c,d in itertools.product(range(2), repeat=4)]

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        R1, R2, I1, I2_ideal = witness
    except Exception:
        return [False, False, False]

    def is_ring(R):
        try:
            if not R or len(R) > 1000: return False
            R_set = list(R)
        except Exception:
            return False
            
        zero = None
        for e in R_set:
            if all(e + a == a for a in R_set) and all(a + e == a for a in R_set):
                zero = e
                break
        if zero is None: return False
        
        has_id = False
        for e in R_set:
            if all(e * a == a and a * e == a for a in R_set):
                has_id = True
                break
        if not has_id: return False
        
        for a in R_set:
            if not any(a + b == zero and b + a == zero for b in R_set):
                return False
            for b in R_set:
                ab_add = a + b
                ab_mul = a * b
                if ab_add not in R_set: return False
                if ab_mul not in R_set: return False
                if ab_add != b + a: return False
                for c in R_set:
                    if ab_add + c != a + (b + c): return False
                    if ab_mul * c != a * (b * c): return False
                    bc_add = b + c
                    if a * bc_add != ab_mul + (a * c): return False
                    if ab_add * c != (a * c) + (b * c): return False
        return True

    def is_subgroup_add(I, R):
        try:
            if not I or len(I) > 1000 or len(R) > 1000: return False
            I_set = list(I)
            R_set = list(R)
        except Exception:
            return False
            
        if not all(x in R_set for x in I_set): return False
        
        zero = None
        for e in R_set:
            if all(e + a == a for a in R_set):
                zero = e
                break
        if zero not in I_set: return False
        
        for i in I_set:
            if not any(i + j == zero for j in I_set): return False
            for j in I_set:
                if (i + j) not in I_set: return False
        return True

    def is_ideal(I, R):
        if not is_subgroup_add(I, R): return False
        I_set = list(I)
        R_set = list(R)
        for i in I_set:
            for r in R_set:
                if (r * i) not in I_set: return False
                if (i * r) not in I_set: return False
        return True

    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(I1, R1)
    except Exception:
        h2 = False
        
    try:
        # The conclusion is that (R_1 x R_2) / (I_1 x I_2) is isomorphic to (R_1 / I_1) x (R_2 / I_2).
        # This requires I_2 to be an ideal of R_2. If I_2 is an additive subgroup but NOT an ideal,
        # the quotient R_2 / I_2 is not a ring, and the isomorphism fails.
        is_sub = is_subgroup_add(I2_ideal, R2)
        is_id = is_ideal(I2_ideal, R2)
        neg_q = is_sub and not is_id
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: I_1 is an ideal of R_1",
    "¬Q: The quotient ring (R_1 x R_2) / (I_1 x I_2) is not isomorphic to (R_1 / I_1) x (R_2 / I_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2