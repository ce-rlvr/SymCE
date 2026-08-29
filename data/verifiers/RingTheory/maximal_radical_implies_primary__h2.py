import itertools
import math
import functools
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def extract_ring(witness):
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        R_obj, I_obj = witness
        if isinstance(R_obj, int):
            n = R_obj
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
            one = 1
            return elements, add, mul, zero, one, list(I_obj)
            
    if isinstance(witness, dict):
        if 'n' in witness and 'I' in witness:
            n = witness['n']
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
            one = 1
            return elements, add, mul, zero, one, list(witness['I'])
            
    if hasattr(witness, 'n') and hasattr(witness, 'I'):
        n = witness.n
        elements = list(range(n))
        add = lambda a, b: (a + b) % n
        mul = lambda a, b: (a * b) % n
        zero = 0
        one = 1
        return elements, add, mul, zero, one, list(witness.I)
        
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero') and hasattr(witness, 'one') and hasattr(witness, 'I'):
        return list(witness.elements), witness.add, witness.mul, witness.zero, witness.one, list(witness.I)
        
    raise ValueError("Unsupported witness format")

def check_H1(elements, add, mul, zero, one):
    if zero not in elements or one not in elements: return False
    for a in elements:
        if add(a, zero) != a: return False
        if mul(a, one) != a: return False
        if mul(one, a) != a: return False
        
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
            if mul(a, b) != mul(b, a): return False
            
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def get_rad(elements, mul, I):
    rad = []
    for x in elements:
        curr = x
        in_rad = False
        for _ in range(len(elements) + 2):
            if curr in I:
                in_rad = True
                break
            curr = mul(curr, x)
        if in_rad:
            rad.append(x)
    return rad

def is_ideal(elements, add, mul, zero, S):
    if not S: return False
    if zero not in S: return False
    for a in S:
        for b in S:
            if add(a, b) not in S: return False
        for r in elements:
            if mul(r, a) not in S: return False
            if mul(a, r) not in S: return False
    return True

def is_maximal_ideal(elements, add, mul, zero, one, S):
    if not is_ideal(elements, add, mul, zero, S): return False
    if len(S) == len(elements): return False
    
    for x in elements:
        if x in S: continue
        has_inv = False
        for y in elements:
            coset = [add(one, s) for s in S]
            if mul(x, y) in coset:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def check_H2(elements, add, mul, zero, one, I):
    rad_I = get_rad(elements, mul, I)
    return is_maximal_ideal(elements, add, mul, zero, one, rad_I)

def is_primary_ideal(elements, add, mul, zero, I, rad_I):
    if not is_ideal(elements, add, mul, zero, I): return False
    if len(I) == len(elements): return False
    
    for a in elements:
        for b in elements:
            if mul(a, b) in I:
                if a not in I and b not in rad_I:
                    return False
    return True

def check_Q(elements, add, mul, zero, one, I):
    rad_I = get_rad(elements, mul, I)
    return is_primary_ideal(elements, add, mul, zero, I, rad_I)

def conditions(witness):
    try:
        elements, add, mul, zero, one, I = extract_ring(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(elements, add, mul, zero, one)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(elements, add, mul, zero, one, I)
    except Exception:
        h2 = False
        
    try:
        q = check_Q(elements, add, mul, zero, one, I)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: The radical of I is a maximal ideal of R",
    "¬Q: I is not a primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2