import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness objects
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

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I is a subset of J",
    "¬Q: J/I is not an ideal of R/I, or (R/I)/(J/I) is not isomorphic to R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(obj):
    if isinstance(obj, (list, set, tuple)):
        return list(obj)
    if hasattr(obj, 'elements'):
        return list(obj.elements)
    return list(obj)

def get_add(R):
    if hasattr(R, 'add'): return R.add
    return lambda a, b: a + b

def get_mul(R):
    if hasattr(R, 'mul'): return R.mul
    return lambda a, b: a * b

def get_eq(R):
    if hasattr(R, 'eq'): return R.eq
    def eq(a, b):
        if hasattr(a, 'equals'):
            return a.equals(b)
        return a == b
    return eq

def get_sub(R):
    if hasattr(R, 'sub'): return R.sub
    add = get_add(R)
    elements = get_elements(R)
    eq_func = get_eq(R)
    
    zero = None
    for x in elements:
        try:
            if eq_func(add(x, x), x):
                zero = x
                break
        except Exception:
            pass
            
    def sub(a, b):
        try:
            res = a - b
            for x in elements:
                if eq_func(res, x):
                    return res
        except Exception:
            pass
            
        if zero is not None:
            for x in elements:
                try:
                    if eq_func(add(b, x), zero) or eq_func(add(x, b), zero):
                        return add(a, x)
                except Exception:
                    pass
        try:
            return a - b
        except Exception:
            return None
    return sub

def parse_witness(witness):
    if isinstance(witness, dict):
        R = witness.get('R', [])
        I = witness.get('I', [])
        J = witness.get('J', [])
        add = witness.get('add', lambda a, b: a + b)
        mul = witness.get('mul', lambda a, b: a * b)
        eq_func = witness.get('eq', lambda a, b: a == b)
        
        if 'sub' in witness:
            sub = witness['sub']
        else:
            zero = None
            for x in R:
                try:
                    if eq_func(add(x, x), x):
                        zero = x
                        break
                except Exception:
                    pass
            def sub(a, b):
                try:
                    res = a - b
                    for x in R:
                        if eq_func(res, x): return res
                except Exception:
                    pass
                if zero is not None:
                    for x in R:
                        try:
                            if eq_func(add(b, x), zero) or eq_func(add(x, b), zero):
                                return add(a, x)
                        except Exception:
                            pass
                try:
                    return a - b
                except Exception:
                    return None
        return R, I, J, add, mul, sub, eq_func
    else:
        R, I, J = witness
        elements = get_elements(R)
        add = get_add(R)
        mul = get_mul(R)
        sub = get_sub(R)
        eq_func = get_eq(R)
        I_elements = get_elements(I)
        J_elements = get_elements(J)
        return elements, I_elements, J_elements, add, mul, sub, eq_func

def is_ideal(R_elements, I_elements, add, mul, sub, eq_func):
    if not I_elements:
        return False
    for a in I_elements:
        if not any(eq_func(a, x) for x in R_elements):
            return False
    for a in I_elements:
        for b in I_elements:
            diff = sub(a, b)
            if not any(eq_func(diff, x) for x in I_elements):
                return False
    for r in R_elements:
        for a in I_elements:
            prod1 = mul(r, a)
            if not any(eq_func(prod1, x) for x in I_elements):
                return False
            prod2 = mul(a, r)
            if not any(eq_func(prod2, x) for x in I_elements):
                return False
    return True

def is_subset(subset, superset, eq_func):
    for a in subset:
        if not any(eq_func(a, x) for x in superset):
            return False
    return True

def coset_eq(r1, r2, I_elements, sub, eq_func):
    diff = sub(r1, r2)
    return any(eq_func(diff, x) for x in I_elements)

def get_reps(R_elements, I_elements, sub, eq_func):
    reps = []
    for r in R_elements:
        if not any(coset_eq(r, rep, I_elements, sub, eq_func) for rep in reps):
            reps.append(r)
    return reps

def get_J_over_I_reps(R_reps, J_elements, I_elements, sub, eq_func):
    J_over_I_reps = []
    for r in R_reps:
        found = False
        for j in J_elements:
            if coset_eq(r, j, I_elements, sub, eq_func):
                found = True
                break
        if found:
            J_over_I_reps.append(r)
    return J_over_I_reps

def is_ideal_quotient(R_reps, J_over_I_reps, I_elements, add, mul, sub, eq_func):
    if not J_over_I_reps:
        return False
    def q_eq(a, b):
        return coset_eq(a, b, I_elements, sub, eq_func)
        
    for a in J_over_I_reps:
        for b in J_over_I_reps:
            diff = sub(a, b)
            if not any(q_eq(diff, x) for x in J_over_I_reps):
                return False
                
    for r in R_reps:
        for a in J_over_I_reps:
            prod1 = mul(r, a)
            if not any(q_eq(prod1, x) for x in J_over_I_reps):
                return False
            prod2 = mul(a, r)
            if not any(q_eq(prod2, x) for x in J_over_I_reps):
                return False
    return True

def get_ring_tables(elements, add, mul, eq_func):
    n = len(elements)
    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            s = add(elements[i], elements[j])
            p = mul(elements[i], elements[j])
            s_idx = next((k for k, x in enumerate(elements) if eq_func(s, x)), -1)
            p_idx = next((k for k, x in enumerate(elements) if eq_func(p, x)), -1)
            if s_idx == -1 or p_idx == -1:
                return None
            add_table[i][j] = s_idx
            mul_table[i][j] = p_idx
    return add_table, mul_table

def are_isomorphic(tables1, tables2):
    if tables1 is None or tables2 is None:
        return False
    add1, mul1 = tables1
    add2, mul2 = tables2
    n = len(add1)
    if len(add2) != n:
        return False
        
    def solve(mapping, used, i):
        if i == n:
            return True
        for j in range(n):
            if not used[j]:
                consistent = True
                for k in range(i):
                    if mapping[add1[i][k]] != -1 and mapping[add1[i][k]] != add2[j][mapping[k]]:
                        consistent = False; break
                    if mapping[add1[k][i]] != -1 and mapping[add1[k][i]] != add2[mapping[k]][j]:
                        consistent = False; break
                    if mapping[mul1[i][k]] != -1 and mapping[mul1[i][k]] != mul2[j][mapping[k]]:
                        consistent = False; break
                    if mapping[mul1[k][i]] != -1 and mapping[mul1[k][i]] != mul2[mapping[k]][j]:
                        consistent = False; break
                if consistent:
                    if mapping[add1[i][i]] != -1 and mapping[add1[i][i]] != add2[j][j]:
                        consistent = False
                    elif mapping[mul1[i][i]] != -1 and mapping[mul1[i][i]] != mul2[j][j]:
                        consistent = False
                        
                if consistent:
                    mapping[i] = j
                    used[j] = True
                    if solve(mapping, used, i + 1):
                        return True
                    mapping[i] = -1
                    used[j] = False
        return False

    mapping = [-1] * n
    used = [False] * n
    return solve(mapping, used, 0)

def build_quotient_ring(R_elements, J_elements, add, mul, sub, eq_func):
    reps = get_reps(R_elements, J_elements, sub, eq_func)
    def q_eq(a, b):
        return coset_eq(a, b, J_elements, sub, eq_func)
    return get_ring_tables(reps, add, mul, q_eq)

def double_quotient_eq(a, b, J_I_reps, I_elements, sub, eq_func):
    diff = sub(a, b)
    for x in J_I_reps:
        if coset_eq(diff, x, I_elements, sub, eq_func):
            return True
    return False

def get_double_reps(R_I_reps, J_I_reps, I_elements, sub, eq_func):
    reps = []
    for r in R_I_reps:
        if not any(double_quotient_eq(r, rep, J_I_reps, I_elements, sub, eq_func) for rep in reps):
            reps.append(r)
    return reps

def build_double_quotient_ring(R_elements, I_elements, J_elements, add, mul, sub, eq_func):
    R_I_reps = get_reps(R_elements, I_elements, sub, eq_func)
    J_I_reps = get_J_over_I_reps(R_I_reps, J_elements, I_elements, sub, eq_func)
    double_reps = get_double_reps(R_I_reps, J_I_reps, I_elements, sub, eq_func)
    
    def dq_eq(a, b):
        return double_quotient_eq(a, b, J_I_reps, I_elements, sub, eq_func)
        
    return get_ring_tables(double_reps, add, mul, dq_eq)

def neg_Q_func(R_elements, I_elements, J_elements, add, mul, sub, eq_func):
    if not is_ideal(R_elements, I_elements, add, mul, sub, eq_func):
        return True
        
    R_I_reps = get_reps(R_elements, I_elements, sub, eq_func)
    J_I_reps = get_J_over_I_reps(R_I_reps, J_elements, I_elements, sub, eq_func)
    
    if not is_ideal_quotient(R_I_reps, J_I_reps, I_elements, add, mul, sub, eq_func):
        return True
        
    if not is_ideal(R_elements, J_elements, add, mul, sub, eq_func):
        return True
        
    tables1 = build_double_quotient_ring(R_elements, I_elements, J_elements, add, mul, sub, eq_func)
    tables2 = build_quotient_ring(R_elements, J_elements, add, mul, sub, eq_func)
    
    if not are_isomorphic(tables1, tables2):
        return True
        
    return False

def conditions(witness):
    try:
        R_elements, I_elements, J_elements, add, mul, sub, eq_func = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ideal(R_elements, I_elements, add, mul, sub, eq_func) and \
             is_ideal(R_elements, J_elements, add, mul, sub, eq_func)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subset(I_elements, J_elements, eq_func)
    except Exception:
        h2 = False
        
    try:
        nq = neg_Q_func(R_elements, I_elements, J_elements, add, mul, sub, eq_func)
    except Exception:
        nq = False
        
    return [h1, h2, nq]