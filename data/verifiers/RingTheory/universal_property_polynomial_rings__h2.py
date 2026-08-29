import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_ring(R):
    if isinstance(R, int):
        if R > 0:
            elements = list(range(R))
            add = lambda x, y: (x + y) % R
            mul = lambda x, y: (x * y) % R
            return elements, add, mul
        else:
            raise ValueError("Ring size must be > 0")
    elif isinstance(R, tuple) and len(R) == 3:
        return R
    else:
        raise ValueError("Invalid ring format")

def check_ring(R):
    if isinstance(R, int):
        if R == 1:
            return True, 0, 0
        elif R > 1:
            return True, 0, 1
        return False, None, None
    try:
        elements, add, mul = get_ring(R)
        elements = list(elements)
        n = len(elements)
        if n == 0: return False, None, None
        
        def a(x, y):
            if isinstance(add, dict): return add[(x, y)]
            return add(x, y)
            
        def m(x, y):
            if isinstance(mul, dict): return mul[(x, y)]
            return mul(x, y)
            
        for x in elements:
            for y in elements:
                axy = a(x, y)
                mxy = m(x, y)
                if axy not in elements: return False, None, None
                if mxy not in elements: return False, None, None
                if axy != a(y, x): return False, None, None
                if mxy != m(y, x): return False, None, None
                
        for x in elements:
            for y in elements:
                for z in elements:
                    if a(a(x, y), z) != a(x, a(y, z)): return False, None, None
                    if m(m(x, y), z) != m(x, m(y, z)): return False, None, None
                    if m(x, a(y, z)) != a(m(x, y), m(x, z)): return False, None, None
                    
        zero = None
        for e in elements:
            if all(a(e, x) == x for x in elements):
                zero = e
                break
        if zero is None: return False, None, None
        
        for x in elements:
            has_inv = False
            for y in elements:
                if a(x, y) == zero:
                    has_inv = True
                    break
            if not has_inv: return False, None, None
            
        one = None
        for e in elements:
            if all(m(e, x) == x for x in elements):
                one = e
                break
        if one is None: return False, None, None
        
        return True, zero, one
    except Exception:
        return False, None, None

def is_ring_homomorphism(phi, R, S):
    try:
        R_elements, R_add, R_mul = get_ring(R)
        S_elements, S_add, S_mul = get_ring(S)
        
        _, _, one_R = check_ring(R)
        _, _, one_S = check_ring(S)
        
        if one_R is None or one_S is None:
            return False
            
        def a_R(x, y):
            if isinstance(R_add, dict): return R_add[(x, y)]
            return R_add(x, y)
        def m_R(x, y):
            if isinstance(R_mul, dict): return R_mul[(x, y)]
            return R_mul(x, y)
        def a_S(x, y):
            if isinstance(S_add, dict): return S_add[(x, y)]
            return S_add(x, y)
        def m_S(x, y):
            if isinstance(S_mul, dict): return S_mul[(x, y)]
            return S_mul(x, y)
            
        def eval_p(r):
            if isinstance(phi, dict): return phi[r]
            return phi(r)
            
        if eval_p(one_R) != one_S:
            return False
            
        for x in R_elements:
            px = eval_p(x)
            if px not in S_elements:
                return False
            for y in R_elements:
                py = eval_p(y)
                
                if eval_p(a_R(x, y)) != a_S(px, py):
                    return False
                if eval_p(m_R(x, y)) != m_S(px, py):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        R, S, phi, s = witness
    except Exception:
        return [False, False, False]
        
    try:
        is_R_comm, _, _ = check_ring(R)
        is_S_comm, _, _ = check_ring(S)
        h1 = bool(is_R_comm and is_S_comm)
    except Exception:
        h1 = False
        
    try:
        S_elements, _, _ = get_ring(S)
        h2 = bool(s in S_elements)
    except Exception:
        h2 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not is_ring_homomorphism(phi, R, S)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: R and S are commutative rings", "H_2: s is an element of S", "not Q: conclusion fails"]
N_HYP = 2
NEG_Q_INDEX = 2