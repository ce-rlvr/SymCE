import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 4:
        n, m, f_dict, J = witness
        if isinstance(n, int) and isinstance(m, int):
            R = list(range(n))
            S = list(range(m))
            add_R = lambda a, b: (a + b) % n
            mul_R = lambda a, b: (a * b) % n
            zero_R = 0
            one_R = 1 % n
            add_S = lambda a, b: (a + b) % m
            mul_S = lambda a, b: (a * b) % m
            zero_S = 0
            one_S = 1 % m
            f = lambda x: f_dict[x]
            return R, S, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S, f, J

    if isinstance(witness, dict):
        if 'n' in witness and 'm' in witness:
            n = witness['n']
            m = witness['m']
            R = list(range(n))
            S = list(range(m))
            add_R = lambda a, b: (a + b) % n
            mul_R = lambda a, b: (a * b) % n
            zero_R = 0
            one_R = 1 % n
            add_S = lambda a, b: (a + b) % m
            mul_S = lambda a, b: (a * b) % m
            zero_S = 0
            one_S = 1 % m
            f_dict = witness['f']
            f = lambda x: f_dict[x]
            J = witness['J']
            return R, S, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S, f, J
        else:
            R = witness['R']
            S = witness['S']
            zero_R = witness['zero_R']
            one_R = witness['one_R']
            zero_S = witness['zero_S']
            one_S = witness['one_S']
            
            def make_op(data, elements):
                if callable(data): return data
                if isinstance(data, dict): return lambda a, b: data[(a, b)]
                if isinstance(data, list): return lambda a, b: data[elements.index(a)][elements.index(b)]
                raise ValueError("Invalid operation data")
                
            add_R = make_op(witness['add_R'], R)
            mul_R = make_op(witness['mul_R'], R)
            add_S = make_op(witness['add_S'], S)
            mul_S = make_op(witness['mul_S'], S)
            
            f_data = witness['f']
            f = f_data if callable(f_data) else lambda x: f_data[x]
            J = witness['J']
            
            return R, S, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S, f, J
            
    return None

def is_ring(elements, add, mul, zero, one):
    if zero not in elements or one not in elements:
        return False
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            if add(a, b) != add(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    for a in elements:
        if mul(a, one) != a or mul(one, a) != a: return False
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    return True

def is_homomorphism(R, S, add_R, mul_R, one_R, add_S, mul_S, one_S, f):
    if f(one_R) != one_S: return False
    for a in R:
        if f(a) not in S: return False
        for b in R:
            if f(add_R(a, b)) != add_S(f(a), f(b)): return False
            if f(mul_R(a, b)) != mul_S(f(a), f(b)): return False
    return True

def is_ideal(R, add_R, mul_R, zero_R, subset):
    if zero_R not in subset: return False
    for a in subset:
        for b in subset:
            if add_R(a, b) not in subset: return False
    for a in subset:
        has_inv = False
        for b in subset:
            if add_R(a, b) == zero_R and add_R(b, a) == zero_R:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in subset:
        for r in R:
            if mul_R(a, r) not in subset: return False
            if mul_R(r, a) not in subset: return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        parsed = parse_witness(witness)
        if parsed is None:
            return [False, False, False]
        R, S, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S, f, J = parsed
    except Exception:
        return [False, False, False]

    try:
        h1 = is_ring(R, add_R, mul_R, zero_R, one_R) and is_ring(S, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    try:
        h2 = is_homomorphism(R, S, add_R, mul_R, one_R, add_S, mul_S, one_S, f)
    except Exception:
        h2 = False

    try:
        f_inv_J = [x for x in R if f(x) in J]
        ker_f = [x for x in R if f(x) == zero_S]
        
        ideal_check = is_ideal(R, add_R, mul_R, zero_R, f_inv_J)
        contains_ker = all(x in f_inv_J for x in ker_f)
        
        q = ideal_check and contains_ker
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "not Q: f^{-1}(J) is not an ideal of R containing ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2