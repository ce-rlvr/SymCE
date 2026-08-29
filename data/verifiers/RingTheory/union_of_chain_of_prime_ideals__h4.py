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

# Top-level setup for Ring Theory
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

class DictRing:
    def __init__(self, d):
        self.elements = d['elements']
        self.zero = d['zero']
        self.one = d['one']
        self.add = d['add']
        self.mul = d['mul']

# Common finite rings that a witness might reference
Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z5 = Z_n(5)
Z6 = Z_n(6)

def is_commutative_ring_with_identity(R):
    try:
        elements = list(R.elements)
        if len(elements) > 100: 
            return False
        zero = R.zero
        one = R.one
        add = R.add
        mul = R.mul
    except Exception:
        return False
        
    if zero not in elements: return False
    if one not in elements: return False
    
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
        if mul(a, one) != a: return False
        if mul(one, a) != a: return False
        
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            ab = add(a, b)
            if ab not in elements: return False
            if ab != add(b, a): return False
            
            mab = mul(a, b)
            if mab not in elements: return False
            if mab != mul(b, a): return False
            
            for c in elements:
                if add(ab, c) != add(a, add(b, c)): return False
                if mul(mab, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mab, mul(a, c)): return False
                if mul(ab, c) != add(mul(a, c), mul(b, c)): return False
                
    return True

def is_ideal(R, I):
    try:
        I_set = set(I)
        elements = set(R.elements)
    except Exception:
        return False
        
    if not I_set.issubset(elements): return False
    if R.zero not in I_set: return False
    
    for x in I_set:
        for y in I_set:
            if R.add(x, y) not in I_set: return False
            
        has_inv = False
        for y in I_set:
            if R.add(x, y) == R.zero and R.add(y, x) == R.zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for r in elements:
            if R.mul(r, x) not in I_set: return False
            if R.mul(x, r) not in I_set: return False
            
    return True

def is_prime_ideal(R, I):
    if not is_ideal(R, I): return False
    try:
        I_set = set(I)
        elements = set(R.elements)
    except Exception:
        return False
        
    if I_set == elements: return False # must be proper
    
    for a in elements:
        for b in elements:
            if R.mul(a, b) in I_set:
                if a not in I_set and b not in I_set:
                    return False
    return True

def conditions(witness):
    R, C, U = None, None, None
    if isinstance(witness, tuple) and len(witness) == 3:
        R, C, U = witness
    elif isinstance(witness, dict):
        R = witness.get('R')
        C = witness.get('C')
        U = witness.get('U')
    else:
        R = getattr(witness, 'R', None)
        C = getattr(witness, 'C', None)
        U = getattr(witness, 'U', None)
        
    if isinstance(R, int):
        R = Z_n(R)
    elif isinstance(R, dict):
        R = DictRing(R)
        
    try:
        h1 = is_commutative_ring_with_identity(R)
    except Exception:
        h1 = False
        
    try:
        if not C:
            h2 = False
        else:
            h2 = True
            for I in C:
                if not is_prime_ideal(R, I):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    try:
        h3 = True
        if C:
            C_sets = [set(I) for I in C]
            for I in C_sets:
                for J in C_sets:
                    if not (I.issubset(J) or J.issubset(I)):
                        h3 = False
                        break
                if not h3: break
    except Exception:
        h3 = False
        
    try:
        neg_q = not is_prime_ideal(R, U)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: C is a non-empty set of prime ideals of R",
    "H_3: C is totally ordered by set inclusion",
    "¬Q: U is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3