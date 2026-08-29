import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
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

def get_field(witness, field):
    if isinstance(witness, dict): return witness[field]
    return getattr(witness, field)

def get_elems(ring):
    if isinstance(ring, dict): return list(ring['elems'])
    if hasattr(ring, 'elems'): return list(ring.elems)
    if hasattr(ring, 'elements'): return list(ring.elements)
    return list(ring)

def get_add(ring):
    if isinstance(ring, dict): return ring['add']
    if hasattr(ring, 'add'): return ring.add
    return ring.add

def get_mul(ring):
    if isinstance(ring, dict): return ring['mul']
    if hasattr(ring, 'mul'): return ring.mul
    return ring.mul

def get_zero(ring):
    if isinstance(ring, dict): return ring['zero']
    if hasattr(ring, 'zero'): return ring.zero
    return ring.zero

def get_one(ring):
    if isinstance(ring, dict): return ring.get('one', None)
    if hasattr(ring, 'one'): return ring.one
    return None

def safe_call(op, x, y):
    if callable(op): return op(x, y)
    if isinstance(op, dict):
        if (x, y) in op: return op[(x, y)]
        if x in op and isinstance(op[x], dict) and y in op[x]: return op[x][y]
    raise ValueError("Operation not defined")

def check_ring_full(ring):
    if hasattr(ring, 'is_ring') and callable(ring.is_ring):
        return ring.is_ring()
    
    try:
        elems = get_elems(ring)
        add_op = get_add(ring)
        mul_op = get_mul(ring)
        zero = get_zero(ring)
        
        if zero not in elems: return False
        
        def add(x, y): return safe_call(add_op, x, y)
        def mul(x, y): return safe_call(mul_op, x, y)

        for a in elems:
            if add(a, zero) != a or add(zero, a) != a: return False
            
            has_inv = False
            for b in elems:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elems:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if ab_add not in elems: return False
                if ab_mul not in elems: return False
                if ab_add != add(b, a): return False
                
                for c in elems:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    except Exception:
        return False
    return True

def check_homomorphism(R, S, f_map):
    try:
        R_elems = get_elems(R)
        R_add = get_add(R)
        R_mul = get_mul(R)
        S_elems = get_elems(S)
        S_add = get_add(S)
        S_mul = get_mul(S)
        
        def apply_f(x):
            if callable(f_map): return f_map(x)
            return f_map[x]
            
        def r_add(x, y): return safe_call(R_add, x, y)
        def r_mul(x, y): return safe_call(R_mul, x, y)
        def s_add(x, y): return safe_call(S_add, x, y)
        def s_mul(x, y): return safe_call(S_mul, x, y)

        for a in R_elems:
            fa = apply_f(a)
            if fa not in S_elems: return False
            for b in R_elems:
                fb = apply_f(b)
                if apply_f(r_add(a, b)) != s_add(fa, fb): return False
                if apply_f(r_mul(a, b)) != s_mul(fa, fb): return False
                
        R_one = get_one(R)
        S_one = get_one(S)
        if R_one is not None and S_one is not None:
            if apply_f(R_one) != S_one:
                return False
    except Exception:
        return False
    return True

def check_H3(R, S_list, f_list, f):
    try:
        R_elems = get_elems(R)
        R_add = get_add(R)
        R_mul = get_mul(R)
        
        def apply_f(x):
            if callable(f): return f(x)
            return f[x]
            
        def apply_fa(fa_map, x):
            if callable(fa_map): return fa_map(x)
            return fa_map[x]

        def r_add(x, y): return safe_call(R_add, x, y)
        def r_mul(x, y): return safe_call(R_mul, x, y)

        for a in R_elems:
            fa = apply_f(a)
            if len(fa) != len(S_list): return False
            for i, S in enumerate(S_list):
                if fa[i] != apply_fa(f_list[i], a):
                    return False
                    
        for a in R_elems:
            for b in R_elems:
                f_a = apply_f(a)
                f_b = apply_f(b)
                f_ab_add = apply_f(r_add(a, b))
                f_ab_mul = apply_f(r_mul(a, b))
                
                for i, S in enumerate(S_list):
                    S_add = get_add(S)
                    S_mul = get_mul(S)
                    def s_add(x, y): return safe_call(S_add, x, y)
                    def s_mul(x, y): return safe_call(S_mul, x, y)
                        
                    if f_ab_add[i] != s_add(f_a[i], f_b[i]): return False
                    if f_ab_mul[i] != s_mul(f_a[i], f_b[i]): return False
    except Exception:
        return False
    return True

def check_conclusion(R, S_list, f_list, f):
    R_elems = get_elems(R)
    
    def apply_f(x):
        if callable(f): return f(x)
        return f[x]
        
    def apply_fa(fa_map, x):
        if callable(fa_map): return fa_map(x)
        return fa_map[x]
        
    prod_zero = tuple(get_zero(S) for S in S_list)
    ker_f = []
    for a in R_elems:
        if apply_f(a) == prod_zero:
            ker_f.append(a)
            
    inter_ker = list(R_elems)
    for i, S in enumerate(S_list):
        S_zero = get_zero(S)
        ker_fa = []
        for a in R_elems:
            if apply_fa(f_list[i], a) == S_zero:
                ker_fa.append(a)
        new_inter = []
        for x in inter_ker:
            if x in ker_fa:
                new_inter.append(x)
        inter_ker = new_inter
        
    for x in ker_f:
        if x not in inter_ker: return False
    for x in inter_ker:
        if x not in ker_f: return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            R, S_list, f_list, f = witness
        else:
            R = get_field(witness, 'R')
            S_list = get_field(witness, 'S_list')
            f_list = get_field(witness, 'f_list')
            f = get_field(witness, 'f')
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = True
        for S in S_list:
            if not check_ring_full(S):
                h1 = False
                break
    except Exception:
        h1 = False
        
    try:
        h2 = True
        if not check_ring_full(R):
            h2 = False
        elif len(f_list) != len(S_list):
            h2 = False
        else:
            for i in range(len(S_list)):
                if not check_homomorphism(R, S_list[i], f_list[i]):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    try:
        h3 = False
        if h2:
            h3 = check_H3(R, S_list, f_list, f)
    except Exception:
        h3 = False
        
    try:
        neg_q = False
        if h2:
            q = check_conclusion(R, S_list, f_list, f)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: {S_alpha} is a family of rings",
    "H_2: {f_alpha} is a family of ring homomorphisms from R to S_alpha",
    "H_3: f is the uniquely induced ring homomorphism to the direct product",
    "¬Q: The kernel of f is NOT the intersection of ker(f_alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3