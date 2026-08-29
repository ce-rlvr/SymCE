import sympy
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a simple FiniteRing class and common finite rings so the witness can easily construct counterexamples.
class FiniteRing:
    def __init__(self, n, elements=None, add_op=None, mul_op=None, zero=0, one=1):
        self.n = n
        self.elements = elements if elements is not None else list(range(n))
        self._add = add_op if add_op is not None else (lambda a, b: (a + b) % n)
        self._mul = mul_op if mul_op is not None else (lambda a, b: (a * b) % n)
        self.zero = zero
        self.one = one

    def add(self, a, b): return self._add(a, b)
    def mul(self, a, b): return self._mul(a, b)
    def __iter__(self): return iter(self.elements)
    def __contains__(self, item): return item in self.elements

Z2 = FiniteRing(2)
Z3 = FiniteRing(3)
Z4 = FiniteRing(4)
Z6 = FiniteRing(6)
trivial_ring = FiniteRing(1, elements=[0], add_op=lambda a,b: 0, mul_op=lambda a,b: 0, zero=0, one=0)

def get_ring_ops(ring):
    if isinstance(ring, dict):
        elements = list(ring['elements'])
        add = ring['add']
        mul = ring['mul']
        zero = ring['zero']
        one = ring['one']
    elif hasattr(ring, 'elements'):
        elements = list(ring.elements)
        add = ring.add
        mul = ring.mul
        zero = ring.zero
        one = ring.one
    else:
        raise ValueError("Unknown ring format")
        
    if len(elements) > 50:
        raise ValueError("Ring too large for verification")
        
    return elements, add, mul, zero, one

def is_ring(ring):
    try:
        elements, add, mul, zero, one = get_ring_ops(ring)
        if zero not in elements or one not in elements: return False
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def is_homomorphism(R, S, f):
    try:
        R_elems, R_add, R_mul, R_zero, R_one = get_ring_ops(R)
        S_elems, S_add, S_mul, S_zero, S_one = get_ring_ops(S)
        
        if f(R_one) != S_one: return False
        for a in R_elems:
            if f(a) not in S_elems: return False
            for b in R_elems:
                if f(R_add(a, b)) != S_add(f(a), f(b)): return False
                if f(R_mul(a, b)) != S_mul(f(a), f(b)): return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
            n = witness.get('n')
        else:
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            f = getattr(witness, 'f', None)
            n = getattr(witness, 'n', None)
            
        if R is None or S is None or f is None or n is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H_2: f is a ring homomorphism from R to S
    try:
        h2 = is_homomorphism(R, S, f)
    except Exception:
        h2 = False

    # H_3: F is the induced ring homomorphism from M_n(R) to M_n(S)
    # We verify that the context (n) is valid for such a homomorphism to exist.
    try:
        h3 = isinstance(n, int) and n >= 1
    except Exception:
        h3 = False

    # ¬Q: The kernel of F is not the matrix ring M_n(K)
    # This occurs if K (the kernel of f) is not a valid ring (i.e., lacks a multiplicative identity).
    try:
        R_elems, R_add, R_mul, R_zero, R_one = get_ring_ops(R)
        S_elems, S_add, S_mul, S_zero, S_one = get_ring_ops(S)
        
        K = [x for x in R_elems if f(x) == S_zero]
        
        has_identity = False
        for e in K:
            is_id = True
            for x in K:
                if R_mul(e, x) != x or R_mul(x, e) != x:
                    is_id = False
                    break
            if is_id:
                has_identity = True
                break
                
        neg_q = not has_identity
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: F is the induced ring homomorphism from M_n(R) to M_n(S)",
    "¬Q: The kernel of F is not the matrix ring M_n(K) (i.e., K is not a ring)"
]

N_HYP = 3
NEG_Q_INDEX = 3