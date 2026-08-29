import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: I_i + I_j = R for all i != j",
    "¬Q: Intersection of ideals is not equal to their product"
]
N_HYP = 2
NEG_Q_INDEX = 2

def to_tuple(M, p):
    def mod(x):
        return int(x) % p if p else int(x)
        
    if hasattr(M, "tolist"):
        return tuple(tuple(mod(x) for x in row) for row in M.tolist())
    elif isinstance(M, (list, tuple)):
        if len(M) > 0 and isinstance(M[0], (list, tuple)):
            return tuple(tuple(mod(x) for x in row) for row in M)
        else:
            return tuple(tuple(mod(x) for x in M),)
    else:
        return mod(M)

def add_el(A, B, p):
    def mod(x):
        return x % p if p else x
        
    if isinstance(A, int):
        return mod(A + B)
    return tuple(tuple(mod(a + b) for a, b in zip(rowA, rowB)) for rowA, rowB in zip(A, B))

def mul_el(A, B, p):
    def mod(x):
        return x % p if p else x
        
    if isinstance(A, int):
        return mod(A * B)
    n = len(A)
    m = len(A[0])
    p_cols = len(B[0])
    res = []
    for i in range(n):
        row = []
        for j in range(p_cols):
            val = mod(sum(A[i][k] * B[k][j] for k in range(m)))
            row.append(val)
        res.append(tuple(row))
    return tuple(res)

def neg_el(A, p):
    def mod(x):
        return x % p if p else x
        
    if isinstance(A, int):
        return mod(-A)
    return tuple(tuple(mod(-val) for val in row) for row in A)

def is_ring(R, p):
    if not R: return False
    R_set = set(R)
    for x in R:
        for y in R:
            if add_el(x, y, p) not in R_set: return False
            if add_el(x, neg_el(y, p), p) not in R_set: return False
            if mul_el(x, y, p) not in R_set: return False
            
    has_id = False
    for e in R:
        is_id = True
        for x in R:
            if mul_el(e, x, p) != x or mul_el(x, e, p) != x:
                is_id = False
                break
        if is_id:
            has_id = True
            break
    if not has_id: return False
    return True

def is_ideal(I, R, p):
    if not I: return False
    I_set = set(I)
    R_set = set(R)
    if not I_set.issubset(R_set): return False
    
    for x in I:
        for y in I:
            if add_el(x, y, p) not in I_set: return False
            if add_el(x, neg_el(y, p), p) not in I_set: return False
            
    for r in R:
        for x in I:
            if mul_el(r, x, p) not in I_set: return False
            if mul_el(x, r, p) not in I_set: return False
    return True

def check_comaximal(ideals, R, p):
    n = len(ideals)
    R_set = set(R)
    for i in range(n):
        for j in range(i + 1, n):
            sum_ij = set()
            for x in ideals[i]:
                for y in ideals[j]:
                    sum_ij.add(add_el(x, y, p))
            if sum_ij != R_set:
                return False
    return True

def additive_closure(generators, p, max_size):
    if not generators: return set()
    
    gen0 = generators[0]
    if isinstance(gen0, int):
        zero = 0
    else:
        zero = tuple(tuple(0 for _ in row) for row in gen0)
        
    closure = {zero}
    queue = [zero]
    
    while queue:
        curr = queue.pop(0)
        for gen in generators:
            nxt = add_el(curr, gen, p)
            if nxt not in closure:
                closure.add(nxt)
                queue.append(nxt)
                if len(closure) > max_size:
                    return closure
    return closure

def check_conclusion(ideals, R, p):
    intersection = set(ideals[0])
    for I in ideals[1:]:
        intersection = intersection.intersection(set(I))
        
    product = set(ideals[0])
    for i in range(1, len(ideals)):
        new_product_gens = set()
        for x in product:
            for y in ideals[i]:
                new_product_gens.add(mul_el(x, y, p))
        product = additive_closure(list(new_product_gens), p, len(R))
        
    return intersection == product

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get("p", 0)
            R_raw = witness["R"]
            ideals_raw = witness["ideals"]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                p, R_raw, ideals_raw = witness
            elif len(witness) == 2:
                R_raw, ideals_raw = witness
                p = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        R = list(set(to_tuple(m, p) for m in R_raw))
        ideals = [list(set(to_tuple(m, p) for m in I)) for I in ideals_raw]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R, p) and len(ideals) >= 2 and all(is_ideal(I, R, p) for I in ideals)
    except Exception:
        h1 = False
        
    try:
        h2 = check_comaximal(ideals, R, p)
    except Exception:
        h2 = False
        
    try:
        neg_q = not check_conclusion(ideals, R, p)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]