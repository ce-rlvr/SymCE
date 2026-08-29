import itertools
import functools
import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: define standard finite rings that a witness might use.
class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = tuple(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

Z2 = FiniteRing((0, 1), lambda a, b: (a + b) % 2, lambda a, b: (a * b) % 2, 0, 1)
Z3 = FiniteRing((0, 1, 2), lambda a, b: (a + b) % 3, lambda a, b: (a * b) % 3, 0, 1)
Z4 = FiniteRing((0, 1, 2, 3), lambda a, b: (a + b) % 4, lambda a, b: (a * b) % 4, 0, 1)
Z6 = FiniteRing((0, 1, 2, 3, 4, 5), lambda a, b: (a + b) % 6, lambda a, b: (a * b) % 6, 0, 1)

# Matrix ring M2(Z2)
M2_Z2_elements = []
for a, b, c, d in itertools.product((0, 1), repeat=4):
    M2_Z2_elements.append(((a, b), (c, d)))

def mat_add(A, B):
    return (((A[0][0] + B[0][0]) % 2, (A[0][1] + B[0][1]) % 2),
            ((A[1][0] + B[1][0]) % 2, (A[1][1] + B[1][1]) % 2))

def mat_mul(A, B):
    return (((A[0][0] * B[0][0] + A[0][1] * B[1][0]) % 2, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % 2),
            ((A[1][0] * B[0][0] + A[1][1] * B[1][0]) % 2, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % 2))

M2_Z2 = FiniteRing(M2_Z2_elements, mat_add, mat_mul, ((0, 0), (0, 0)), ((1, 0), (0, 1)))

def is_ring(R):
    try:
        elements = R.elements
        add = R.add
        mul = R.mul
        zero = R.zero
        one = R.one
        if zero not in elements or one not in elements: 
            return False
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

def is_homomorphism(f, R, S):
    try:
        f_func = lambda a: f[a] if isinstance(f, dict) else f(a)
        if f_func(R.one) != S.one: 
            return False
        for a in R.elements:
            if f_func(a) not in S.elements: 
                return False
            for b in R.elements:
                if f_func(R.add(a, b)) != S.add(f_func(a), f_func(b)): return False
                if f_func(R.mul(a, b)) != S.mul(f_func(a), f_func(b)): return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a tuple: (R, S, f, x)
    where R and S are rings, f is a homomorphism from R to S, and x is an element of R.
    """
    try:
        R, S, f, x_elem = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R and S are rings, and x is an element of R
    try:
        h1 = is_ring(R) and is_ring(S) and (x_elem in R.elements)
    except Exception:
        h1 = False
        
    # H_2: f: R -> S is a ring homomorphism
    try:
        h2 = is_homomorphism(f, R, S)
    except Exception:
        h2 = False
        
    # ¬Q: f(x) is NOT a nilpotent element in S
    try:
        f_func = lambda a: f[a] if isinstance(f, dict) else f(a)
        fx = f_func(x_elem)
        
        is_nilp = False
        current = fx
        # In a finite ring of size N, if an element is nilpotent, 
        # it must reach 0 within N multiplications.
        for _ in range(len(S.elements) + 1):
            if current == S.zero:
                is_nilp = True
                break
            current = S.mul(current, fx)
            
        neg_q = not is_nilp
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings and x is in R",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: f(x) is not a nilpotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2