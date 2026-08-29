import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def get_add(R):
    if hasattr(R, 'add'):
        return R.add
    else:
        return lambda a, b: a + b

def get_mul(R):
    if hasattr(R, 'mul'):
        return R.mul
    else:
        return lambda a, b: a * b

def get_zero(R):
    if hasattr(R, 'zero'):
        return R.zero
    elif hasattr(R, 'elements'):
        try:
            elements = list(R.elements)
            add = get_add(R)
            for z in elements:
                if all(add(a, z) == a and add(z, a) == a for a in elements):
                    return z
        except Exception:
            pass
    return None

def is_ring(R):
    try:
        if not hasattr(R, 'elements'):
            return False
        elements = list(R.elements)
        add = get_add(R)
        mul = get_mul(R)
        zero = get_zero(R)
        if zero is None or zero not in elements:
            return False
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if ab_add not in elements: return False
                if ab_mul not in elements: return False
                if ab_add != add(b, a): return False
                for c in elements:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def jacobson_radical(R):
    elements = list(R.elements)
    add = get_add(R)
    mul = get_mul(R)
    
    J = []
    for x in elements:
        is_in_J = True
        for y in elements:
            xy = mul(x, y)
            rqr = False
            for z in elements:
                if add(xy, z) == mul(xy, z):
                    rqr = True
                    break
            if not rqr:
                is_in_J = False
                break
        if is_in_J:
            J.append(x)
    return J

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R1 = witness.get('R1')
            R2 = witness.get('R2')
            R = witness.get('R')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R1, R2, R = witness
        else:
            R1 = getattr(witness, 'R1', None)
            R2 = getattr(witness, 'R2', None)
            R = getattr(witness, 'R', None)
            
        if R1 is None or R2 is None or R is None:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: R1 and R2 are rings
    try:
        h1_ok = is_ring(R1) and is_ring(R2)
    except Exception:
        h1_ok = False

    # neg_Q: The Jacobson radical of R is NOT equal to J(R1) x J(R2)
    try:
        if not is_ring(R):
            neg_q_ok = False
        else:
            J_R1 = jacobson_radical(R1)
            J_R2 = jacobson_radical(R2)
            J_R = jacobson_radical(R)
            
            prod = []
            for a in J_R1:
                for b in J_R2:
                    prod.append((a, b))
                    
            def is_subset(A, B):
                for a in A:
                    if a not in B:
                        return False
                return True
                
            q_ok = is_subset(J_R, prod) and is_subset(prod, J_R)
            neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "¬Q: The Jacobson radical of R is not equal to J(R1) x J(R2)"
]

N_HYP = 1
NEG_Q_INDEX = 1