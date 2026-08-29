import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(w, names):
    if isinstance(w, dict):
        for name in names:
            if name in w:
                return w[name]
    else:
        for name in names:
            if hasattr(w, name):
                return getattr(w, name)
    raise ValueError(f"Missing attribute: {names}")

def apply_op(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    return op(a, b)

def apply_f(f, a):
    if isinstance(f, dict):
        return f[a]
    return f(a)

def check_h1(w):
    R = get_attr(w, ['R', 'ring_R'])
    S = get_attr(w, ['S', 'ring_S'])
    R_add = get_attr(w, ['R_add', 'add_R'])
    R_mul = get_attr(w, ['R_mul', 'mul_R'])
    S_add = get_attr(w, ['S_add', 'add_S'])
    S_mul = get_attr(w, ['S_mul', 'mul_S'])
    f = get_attr(w, ['f', 'phi'])
    
    for a in R:
        fa = apply_f(f, a)
        if fa not in S:
            return False
        for b in R:
            fb = apply_f(f, b)
            if apply_f(f, apply_op(R_add, a, b)) != apply_op(S_add, fa, fb):
                return False
            if apply_f(f, apply_op(R_mul, a, b)) != apply_op(S_mul, fa, fb):
                return False
    return True

def check_h2(w):
    R = get_attr(w, ['R', 'ring_R'])
    S = get_attr(w, ['S', 'ring_S'])
    R_mul = get_attr(w, ['R_mul', 'mul_R'])
    S_mul = get_attr(w, ['S_mul', 'mul_S'])
    f = get_attr(w, ['f', 'phi'])
    id_R = get_attr(w, ['id_R', '1_R', 'one_R'])
    id_S = get_attr(w, ['id_S', '1_S', 'one_S'])
    
    for a in R:
        if apply_op(R_mul, id_R, a) != a or apply_op(R_mul, a, id_R) != a:
            return False
            
    for b in S:
        if apply_op(S_mul, id_S, b) != b or apply_op(S_mul, b, id_S) != b:
            return False
            
    return apply_f(f, id_R) == id_S

def check_h3(w):
    R = get_attr(w, ['R', 'ring_R'])
    R_mul = get_attr(w, ['R_mul', 'mul_R'])
    u = get_attr(w, ['u'])
    id_R = get_attr(w, ['id_R', '1_R', 'one_R'])
    
    if u not in R:
        return False
        
    for v in R:
        if apply_op(R_mul, u, v) == id_R and apply_op(R_mul, v, u) == id_R:
            return True
    return False

def check_neg_q(w):
    S = get_attr(w, ['S', 'ring_S'])
    S_mul = get_attr(w, ['S_mul', 'mul_S'])
    f = get_attr(w, ['f', 'phi'])
    u = get_attr(w, ['u'])
    id_S = get_attr(w, ['id_S', '1_S', 'one_S'])
    
    fu = apply_f(f, u)
    if fu not in S:
        return False
        
    for v in S:
        if apply_op(S_mul, fu, v) == id_S and apply_op(S_mul, v, fu) == id_S:
            return False
            
    return True

def conditions(witness):
    try:
        h1 = bool(check_h1(witness))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_h2(witness))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_h3(witness))
    except Exception:
        h3 = False

    try:
        neg_q = bool(check_neg_q(witness))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "H_2: f maps the identity of R to the identity of S",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S"
]

N_HYP = 3
NEG_Q_INDEX = 3