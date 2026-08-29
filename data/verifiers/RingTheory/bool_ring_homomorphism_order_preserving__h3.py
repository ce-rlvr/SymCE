import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import sympy.abc
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

class RingWrapper:
    def __init__(self, elements, add_func, mul_func):
        self.elements = elements
        self.add = add_func
        self.mul = mul_func

def apply_f(f, a):
    if isinstance(f, dict):
        return f[a]
    elif callable(f):
        return f(a)
    else:
        return f[a]

def parse_witness(witness):
    if isinstance(witness, dict):
        if 'R_add' in witness:
            R = RingWrapper(list(range(len(witness['R_add']))), lambda a, b: witness['R_add'][a][b], lambda a, b: witness['R_mul'][a][b])
            S = RingWrapper(list(range(len(witness['S_add']))), lambda a, b: witness['S_add'][a][b], lambda a, b: witness['S_mul'][a][b])
            return R, S, witness['f'], witness['x'], witness['y']
        else:
            R = RingWrapper(list(witness['R']), lambda a, b: a + b, lambda a, b: a * b)
            S = RingWrapper(list(witness['S']), lambda a, b: a + b, lambda a, b: a * b)
            return R, S, witness['f'], witness['x'], witness['y']
    elif hasattr(witness, 'R_add'):
        R = RingWrapper(list(range(len(witness.R_add))), lambda a, b: witness.R_add[a][b], lambda a, b: witness.R_mul[a][b])
        S = RingWrapper(list(range(len(witness.S_add))), lambda a, b: witness.S_add[a][b], lambda a, b: witness.S_mul[a][b])
        return R, S, witness.f, witness.x, witness.y
    elif hasattr(witness, 'R'):
        R = RingWrapper(list(witness.R), lambda a, b: a + b, lambda a, b: a * b)
        S = RingWrapper(list(witness.S), lambda a, b: a + b, lambda a, b: a * b)
        return R, S, witness.f, witness.x, witness.y
    elif isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) == 7:
            R_add, R_mul, S_add, S_mul, f, x, y = witness
            R = RingWrapper(list(range(len(R_add))), lambda a, b: R_add[a][b], lambda a, b: R_mul[a][b])
            S = RingWrapper(list(range(len(S_add))), lambda a, b: S_add[a][b], lambda a, b: S_mul[a][b])
            return R, S, f, x, y
        elif len(witness) == 5:
            R_obj, S_obj, f, x, y = witness
            R = RingWrapper(list(R_obj), lambda a, b: a + b, lambda a, b: a * b)
            S = RingWrapper(list(S_obj), lambda a, b: a + b, lambda a, b: a * b)
            return R, S, f, x, y
    raise ValueError("Cannot parse witness")

def check_boolean_ring(ring: RingWrapper):
    elements = ring.elements
    n = len(elements)
    if n == 0: return False
    
    zero = None
    for a in elements:
        is_zero = True
        for b in elements:
            try:
                sum_ab = ring.add(a, b)
                prod_ab = ring.mul(a, b)
            except Exception:
                return False
            if sum_ab not in elements: return False
            if prod_ab not in elements: return False
            if sum_ab != b: is_zero = False
        if is_zero:
            zero = a
            
    if zero is None: return False
    
    for a in elements:
        has_inv = False
        for b in elements:
            if ring.add(a, b) != ring.add(b, a): return False
            if ring.add(a, b) == zero: has_inv = True
        if not has_inv: return False
        
    for a in elements:
        for b in elements:
            for c in elements:
                if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): return False
                if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): return False
                if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): return False
                if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): return False
                
    for a in elements:
        if ring.mul(a, a) != a: return False
        
    return True

def check_homomorphism(R: RingWrapper, S: RingWrapper, f):
    for a in R.elements:
        try:
            fa = apply_f(f, a)
        except Exception:
            return False
        if fa not in S.elements: return False
        for b in R.elements:
            try:
                fb = apply_f(f, b)
                if apply_f(f, R.add(a, b)) != S.add(fa, fb): return False
                if apply_f(f, R.mul(a, b)) != S.mul(fa, fb): return False
            except Exception:
                return False
    return True

def check_x_le_y(R: RingWrapper, x, y):
    if x not in R.elements or y not in R.elements: return False
    return R.mul(x, y) == x

def check_fx_le_fy(S: RingWrapper, f, x, y):
    try:
        fx = apply_f(f, x)
        fy = apply_f(f, y)
    except Exception:
        return False
    if fx not in S.elements or fy not in S.elements: return False
    return S.mul(fx, fy) == fx

def conditions(witness) -> list[bool]:
    try:
        R, S, f, x, y = parse_witness(witness)
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = check_boolean_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = check_boolean_ring(S)
    except Exception:
        h2 = False
        
    try:
        h3 = check_homomorphism(R, S, f)
    except Exception:
        h3 = False
        
    try:
        h4 = check_x_le_y(R, x, y)
    except Exception:
        h4 = False
        
    try:
        q = check_fx_le_fy(S, f, x, y)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a Boolean ring",
    "H_3: f is a ring homomorphism from R to S",
    "H_4: x <= y in R",
    "¬Q: f(x) is not <= f(y) in S"
]

N_HYP = 4
NEG_Q_INDEX = 4