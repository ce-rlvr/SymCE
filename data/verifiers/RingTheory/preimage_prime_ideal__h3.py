import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class ZMod:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def __str__(self): 
        return f"ZMod({self.n})"
        
    def __repr__(self): 
        return self.__str__()

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

# Pre-instantiate common finite rings
Z2 = ZMod(2)
Z3 = ZMod(3)
Z4 = ZMod(4)
Z5 = ZMod(5)
Z6 = ZMod(6)
Z7 = ZMod(7)
Z8 = ZMod(8)
Z9 = ZMod(9)
Z10 = ZMod(10)
Z12 = ZMod(12)

def is_comm_ring_with_id(R):
    try:
        if not hasattr(R, 'elements'): return False
        elements = R.elements
        zero = R.zero
        one = R.one
        if zero not in elements or one not in elements: return False
        
        for a in elements:
            if R.add(a, zero) != a or R.add(zero, a) != a: return False
            if R.mul(a, one) != a or R.mul(one, a) != a: return False
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero and R.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for a in elements:
            for b in elements:
                if R.add(a, b) not in elements: return False
                if R.mul(a, b) not in elements: return False
                if R.add(a, b) != R.add(b, a): return False
                if R.mul(a, b) != R.mul(b, a): return False
                
        for a in elements:
            for b in elements:
                ab_add = R.add(a, b)
                ab_mul = R.mul(a, b)
                for c in elements:
                    if R.add(ab_add, c) != R.add(a, R.add(b, c)): return False
                    if R.mul(ab_mul, c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(ab_mul, R.mul(a, c)): return False
        return True
    except Exception:
        return False

def is_homomorphism(R, S, f_dict):
    try:
        if not all(a in f_dict for a in R.elements): return False
        if not all(f_dict[a] in S.elements for a in R.elements): return False
        if f_dict[R.one] != S.one: return False
        for a in R.elements:
            for b in R.elements:
                if f_dict[R.add(a, b)] != S.add(f_dict[a], f_dict[b]): return False
                if f_dict[R.mul(a, b)] != S.mul(f_dict[a], f_dict[b]): return False
        return True
    except Exception:
        return False

def is_ideal(R, I):
    try:
        if not I: return False
        if not all(x in R.elements for x in I): return False
        if R.zero not in I: return False
        for a in I:
            for b in I:
                minus_b = None
                for x in R.elements:
                    if R.add(b, x) == R.zero:
                        minus_b = x
                        break
                if minus_b is None: return False
                if R.add(a, minus_b) not in I: return False
        for a in I:
            for r in R.elements:
                if R.mul(a, r) not in I: return False
                if R.mul(r, a) not in I: return False
        return True
    except Exception:
        return False

def is_prime_ideal(R, I):
    try:
        if not is_ideal(R, I): return False
        if set(I) == set(R.elements): return False
        for a in R.elements:
            for b in R.elements:
                if R.mul(a, b) in I:
                    if a not in I and b not in I:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness should be a tuple: (R, S, f, P)
    where R and S are ring objects (like ZMod),
    f is a dictionary or callable representing the homomorphism R -> S,
    and P is an iterable representing a subset of S.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        R, S, f, P = witness
    except Exception:
        return [False, False, False]
    
    # H1: R and S are commutative rings with identity
    try:
        h1 = is_comm_ring_with_id(R) and is_comm_ring_with_id(S)
    except Exception:
        h1 = False
        
    # H2: f is a ring homomorphism
    try:
        if not isinstance(f, dict):
            f_dict = {a: f(a) for a in R.elements}
        else:
            f_dict = f
        h2 = is_homomorphism(R, S, f_dict)
    except Exception:
        h2 = False
        
    # neg_Q: The preimage f^{-1}(P) is NOT a prime ideal of R
    try:
        if not isinstance(f, dict):
            f_dict = {a: f(a) for a in R.elements}
        else:
            f_dict = f
            
        if not hasattr(P, '__iter__'):
            neg_q = False
        elif not all(p in S.elements for p in P):
            neg_q = False
        else:
            preimage = [r for r in R.elements if f_dict[r] in P]
            neg_q = not is_prime_ideal(R, preimage)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: The preimage f^{-1}(P) is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2