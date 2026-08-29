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

class Ring:
    def __init__(self, elements, add_func, mul_func, zero, one):
        self.elements = list(elements)
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero = zero
        self.one = one

    def add(self, x, y):
        return self.add_func(x, y)

    def mul(self, x, y):
        return self.mul_func(x, y)

class RingHomomorphism:
    def __init__(self, R, S, mapping):
        self.R = R
        self.S = S
        self.mapping = mapping
        
    def __call__(self, x):
        if isinstance(self.mapping, dict):
            return self.mapping[x]
        return self.mapping(x)

def make_Zn(n):
    return Ring(
        elements=list(range(n)),
        add_func=lambda x, y: (x + y) % n,
        mul_func=lambda x, y: (x * y) % n,
        zero=0,
        one=1
    )

# Standard finite rings for witness construction
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)

def is_comm_ring_with_id(ring):
    try:
        elements = list(ring.elements)
        zero = ring.zero
        one = ring.one
        if zero not in elements or one not in elements: return False
        
        # Identity
        for x in elements:
            if ring.add(x, zero) != x or ring.add(zero, x) != x: return False
            if ring.mul(x, one) != x or ring.mul(one, x) != x: return False
            
        # Commutativity
        for x in elements:
            for y in elements:
                if ring.add(x, y) != ring.add(y, x): return False
                if ring.mul(x, y) != ring.mul(y, x): return False
                
        # Associativity and Distributivity
        for x in elements:
            for y in elements:
                for z in elements:
                    if ring.add(ring.add(x, y), z) != ring.add(x, ring.add(y, z)): return False
                    if ring.mul(ring.mul(x, y), z) != ring.mul(x, ring.mul(y, z)): return False
                    if ring.mul(x, ring.add(y, z)) != ring.add(ring.mul(x, y), ring.mul(x, z)): return False
                    
        # Additive inverse
        for x in elements:
            has_inv = False
            for y in elements:
                if ring.add(x, y) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True
    except Exception:
        return False

def is_integral_domain(ring):
    try:
        if not is_comm_ring_with_id(ring): return False
        if ring.zero == ring.one: return False
        elements = list(ring.elements)
        for x in elements:
            if x == ring.zero: continue
            for y in elements:
                if y == ring.zero: continue
                if ring.mul(x, y) == ring.zero: return False
        return True
    except Exception:
        return False

def is_ring_homomorphism(f):
    try:
        R = f.R
        S = f.S
        elements = list(R.elements)
        for x in elements:
            for y in elements:
                if f(R.add(x, y)) != S.add(f(x), f(y)): return False
                if f(R.mul(x, y)) != S.mul(f(x), f(y)): return False
        return True
    except Exception:
        return False

def is_prime_ideal(R, subset):
    try:
        elements = list(R.elements)
        # Proper ideal check
        if len(subset) == len(elements): return False
        if R.one in subset: return False
        if R.zero not in subset: return False
        
        # Ideal properties
        for x in subset:
            for y in subset:
                if R.add(x, y) not in subset: return False
        for x in subset:
            for r in elements:
                if R.mul(r, x) not in subset: return False
                if R.mul(x, r) not in subset: return False
                
        # Prime property
        for a in elements:
            for b in elements:
                if R.mul(a, b) in subset:
                    if a not in subset and b not in subset:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    # Allow witness to be a tuple (R, S, mapping) for convenience
    if isinstance(witness, tuple) and len(witness) == 3:
        witness = RingHomomorphism(witness[0], witness[1], witness[2])

    try:
        h1 = is_comm_ring_with_id(witness.R) and is_comm_ring_with_id(witness.S)
    except Exception:
        h1 = False

    try:
        h2 = is_integral_domain(witness.S)
    except Exception:
        h2 = False

    try:
        h3 = is_ring_homomorphism(witness)
    except Exception:
        h3 = False

    try:
        elements = list(witness.R.elements)
        kernel = [x for x in elements if witness(x) == witness.S.zero]
        neg_q = not is_prime_ideal(witness.R, kernel)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is an integral domain",
    "H_3: f: R -> S is a ring homomorphism",
    "¬Q: The kernel of f is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3