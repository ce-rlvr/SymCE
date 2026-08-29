import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class Z_n:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n

def get_ring(R):
    if isinstance(R, int) or (hasattr(R, 'is_Integer') and R.is_Integer):
        return Z_n(int(R))
    return R

def check_ring(R):
    try:
        elements = list(R.elements)
        if len(elements) > 100:
            return False
            
        zero = R.zero
        one = R.one
        
        for a in elements:
            for b in elements:
                if R.add(a, b) != R.add(b, a): return False
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
                    
        for a in elements:
            if R.add(a, zero) != a: return False
            if R.mul(a, one) != a: return False
            if R.mul(one, a) != a: return False
            if not any(R.add(a, b) == zero for b in elements): return False
            
        return True
    except Exception:
        return False

def check_homomorphism(R, S, f):
    try:
        R_elems = list(R.elements)
        S_elems = list(S.elements)
        if len(R_elems) > 100 or len(S_elems) > 100:
            return False
            
        def apply_f(x):
            if isinstance(f, dict):
                return f[x]
            elif isinstance(f, (list, tuple)):
                return f[x]
            return f(x)
        
        mapped = []
        for a in R_elems:
            fa = apply_f(a)
            if fa not in S_elems: return False
            mapped.append(fa)
            
        for b in S_elems:
            if b not in mapped: return False
            
        if apply_f(R.one) != S.one: return False
        
        for a in R_elems:
            for b in R_elems:
                if apply_f(R.add(a, b)) != S.add(apply_f(a), apply_f(b)): return False
                if apply_f(R.mul(a, b)) != S.mul(apply_f(a), apply_f(b)): return False
                
        return True
    except Exception:
        return False

def is_von_neumann_regular(S):
    try:
        S_elems = list(S.elements)
        if len(S_elems) > 100:
            return False
            
        for a in S_elems:
            if not any(S.mul(S.mul(a, x), a) == a for x in S_elems):
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        R_obj, S_obj, f = witness
        R = get_ring(R_obj)
        S = get_ring(S_obj)
    except Exception:
        return [False, False, False]

    try:
        h1 = check_ring(R) and check_ring(S)
    except Exception:
        h1 = False

    try:
        h2 = check_homomorphism(R, S, f)
    except Exception:
        h2 = False

    try:
        if not check_ring(S):
            neg_q = False
        else:
            neg_q = not is_von_neumann_regular(S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "¬Q: S is not a von Neumann regular ring"
]

N_HYP = 2
NEG_Q_INDEX = 2