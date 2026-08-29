import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def extract_witness(witness):
    if isinstance(witness, dict):
        w = witness
    else:
        w = {k: getattr(witness, k) for k in ['R_set', 'R_add', 'R_mul', 'M_set', 'M_add', 'action_L', 'action_R', 'r', 'm'] if hasattr(witness, k)}
        
    def make_callable(op):
        if callable(op):
            return op
        elif isinstance(op, dict):
            return lambda x, y: op[(x, y)]
        else:
            return lambda x, y: op[x][y]
            
    return {
        'R_set': list(w['R_set']),
        'R_add': make_callable(w['R_add']),
        'R_mul': make_callable(w['R_mul']),
        'M_set': list(w['M_set']),
        'M_add': make_callable(w['M_add']),
        'action_L': make_callable(w['action_L']),
        'action_R': make_callable(w['action_R']),
        'r': w['r'],
        'm': w['m']
    }

def check_ring(R_set, R_add, R_mul):
    if not R_set: return False
    if len(R_set) > 50: return False
    # closure
    for x in R_set:
        for y in R_set:
            if R_add(x, y) not in R_set: return False
            if R_mul(x, y) not in R_set: return False
    # commutative add
    for x in R_set:
        for y in R_set:
            if R_add(x, y) != R_add(y, x): return False
    # associative add
    for x in R_set:
        for y in R_set:
            for z in R_set:
                if R_add(R_add(x, y), z) != R_add(x, R_add(y, z)): return False
    # identity add
    zero = None
    for e in R_set:
        if all(R_add(e, x) == x and R_add(x, e) == x for x in R_set):
            zero = e
            break
    if zero is None: return False
    # inverse add
    for x in R_set:
        if not any(R_add(x, y) == zero for y in R_set): return False
    # associative mul
    for x in R_set:
        for y in R_set:
            for z in R_set:
                if R_mul(R_mul(x, y), z) != R_mul(x, R_mul(y, z)): return False
    # distributive
    for x in R_set:
        for y in R_set:
            for z in R_set:
                if R_mul(x, R_add(y, z)) != R_add(R_mul(x, y), R_mul(x, z)): return False
                if R_mul(R_add(x, y), z) != R_add(R_mul(x, z), R_mul(y, z)): return False
    return True

def check_bimodule(R_set, R_add, R_mul, M_set, M_add, action_L, action_R):
    if not M_set: return False
    if len(M_set) > 50: return False
    
    # M_add closure
    for x in M_set:
        for y in M_set:
            if M_add(x, y) not in M_set: return False
            
    # M_add commutative
    for x in M_set:
        for y in M_set:
            if M_add(x, y) != M_add(y, x): return False
            
    # M_add associative
    for x in M_set:
        for y in M_set:
            for z in M_set:
                if M_add(M_add(x, y), z) != M_add(x, M_add(y, z)): return False
                
    # M_add identity
    zero_M = None
    for e in M_set:
        if all(M_add(e, x) == x and M_add(x, e) == x for x in M_set):
            zero_M = e
            break
    if zero_M is None: return False
    
    # M_add inverse
    for x in M_set:
        if not any(M_add(x, y) == zero_M for y in M_set): return False
        
    # action closure
    for r in R_set:
        for m in M_set:
            if action_L(r, m) not in M_set: return False
            if action_R(m, r) not in M_set: return False
            
    # action_L bilinear
    for r in R_set:
        for s in R_set:
            for m in M_set:
                if action_L(R_add(r, s), m) != M_add(action_L(r, m), action_L(s, m)): return False
    for r in R_set:
        for m in M_set:
            for n in M_set:
                if action_L(r, M_add(m, n)) != M_add(action_L(r, m), action_L(r, n)): return False
                
    # action_R bilinear
    for m in M_set:
        for r in R_set:
            for s in R_set:
                if action_R(m, R_add(r, s)) != M_add(action_R(m, r), action_R(m, s)): return False
    for m in M_set:
        for n in M_set:
            for r in R_set:
                if action_R(M_add(m, n), r) != M_add(action_R(m, r), action_R(n, r)): return False
                
    # associative actions
    for r in R_set:
        for s in R_set:
            for m in M_set:
                if action_L(R_mul(r, s), m) != action_L(r, action_L(s, m)): return False
                if action_R(m, R_mul(r, s)) != action_R(action_R(m, r), s): return False
    for r in R_set:
        for m in M_set:
            for s in R_set:
                if action_L(r, action_R(m, s)) != action_R(action_L(r, m), s): return False
                
    return True

def check_neg_Q(R_set, R_mul, M_set, M_add, action_L, action_R, r, m):
    # Find identity of R
    one_R = None
    for e in R_set:
        if all(R_mul(e, x) == x and R_mul(x, e) == x for x in R_set):
            one_R = e
            break
            
    if one_R is None:
        r_is_unit = False
    else:
        r_is_unit = any(R_mul(r, s) == one_R and R_mul(s, r) == one_R for s in R_set)
        
    # Find identity of R \ltimes M
    RM_set = [(x, y) for x in R_set for y in M_set]
    def RM_mul(a, b):
        r1, m1 = a
        r2, m2 = b
        return (R_mul(r1, r2), M_add(action_L(r1, m2), action_R(m1, r2)))
        
    one_RM = None
    # Optimization: the R-component of the identity must be one_R
    if one_R is not None:
        candidates = [(one_R, y) for y in M_set]
        for e in candidates:
            if all(RM_mul(e, x) == x and RM_mul(x, e) == x for x in RM_set):
                one_RM = e
                break
                
    if one_RM is None:
        rm_is_unit = False
    else:
        rm_is_unit = any(RM_mul((r, m), s) == one_RM and RM_mul(s, (r, m)) == one_RM for s in RM_set)
        
    return rm_is_unit != r_is_unit

def conditions(witness):
    try:
        w = extract_witness(witness)
        R_set = w['R_set']
        R_add = w['R_add']
        R_mul = w['R_mul']
        M_set = w['M_set']
        M_add = w['M_add']
        action_L = w['action_L']
        action_R = w['action_R']
        r = w['r']
        m = w['m']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_ring(R_set, R_add, R_mul)
    except Exception:
        h1 = False
        
    try:
        h2 = check_bimodule(R_set, R_add, R_mul, M_set, M_add, action_L, action_R)
    except Exception:
        h2 = False
        
    try:
        h3 = (r in R_set) and (m in M_set)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(R_set, R_mul, M_set, M_add, action_L, action_R, r, m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is an R-bimodule",
    "H_3: (r, m) is an element of R \\ltimes M",
    "¬Q: (r, m) is a unit in R \\ltimes M iff r is a unit in R is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3