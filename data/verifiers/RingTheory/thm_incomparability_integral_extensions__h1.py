import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_S(witness):
    if isinstance(witness, dict): return witness.get('S')
    if hasattr(witness, 'S'): return witness.S
    if isinstance(witness, tuple) and len(witness) >= 2: return witness[1]
    return None

def get_R(witness):
    if isinstance(witness, dict): return witness.get('R')
    if hasattr(witness, 'R'): return witness.R
    if isinstance(witness, tuple) and len(witness) >= 1: return witness[0]
    return None

def get_Q1(witness):
    if isinstance(witness, dict): return witness.get('Q1')
    if hasattr(witness, 'Q1'): return witness.Q1
    if isinstance(witness, tuple) and len(witness) >= 3: return witness[2]
    return None

def get_Q2(witness):
    if isinstance(witness, dict): return witness.get('Q2')
    if hasattr(witness, 'Q2'): return witness.Q2
    if isinstance(witness, tuple) and len(witness) >= 4: return witness[3]
    return None

def get_add(witness):
    if isinstance(witness, dict) and 'add' in witness: return witness['add']
    if hasattr(witness, 'add'): return witness.add
    return lambda a, b: a + b

def get_mul(witness):
    if isinstance(witness, dict) and 'mul' in witness: return witness['mul']
    if hasattr(witness, 'mul'): return witness.mul
    return lambda a, b: a * b

def get_zero(witness):
    if isinstance(witness, dict) and 'zero' in witness: return witness['zero']
    if hasattr(witness, 'zero'): return witness.zero
    S = get_S(witness)
    if S:
        add = get_add(witness)
        eq = get_eq(witness)
        for e in S:
            if all(eq(add(e, _x), _x) and eq(add(_x, e), _x) for _x in S):
                return e
    return 0

def get_eq(witness):
    if isinstance(witness, dict) and 'eq' in witness: return witness['eq']
    if hasattr(witness, 'eq'): return witness.eq
    return lambda a, b: a == b

def check_subring(witness):
    if hasattr(witness, 'is_subring'): return witness.is_subring()
    if isinstance(witness, dict) and 'is_subring' in witness: return witness['is_subring']()
    
    R = get_R(witness)
    S = get_S(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    zero = get_zero(witness)
    eq = get_eq(witness)
    
    for r in R:
        if not any(eq(r, s) for s in S): return False
    if not any(eq(r, zero) for r in R): return False
    for a in R:
        has_neg = False
        for b in R:
            if eq(add(a, b), zero): has_neg = True
            if not any(eq(add(a, b), r) for r in R): return False
            if not any(eq(mul(a, b), r) for r in R): return False
        if not has_neg: return False
    return True

def check_integral_extension(witness):
    if hasattr(witness, 'is_integral_extension'): return witness.is_integral_extension()
    if isinstance(witness, dict) and 'is_integral_extension' in witness: return witness['is_integral_extension']()
    
    R = get_R(witness)
    S = get_S(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    zero = get_zero(witness)
    eq = get_eq(witness)
    
    one = None
    for e in S:
        if all(eq(mul(e, _x), _x) and eq(mul(_x, e), _x) for _x in S):
            one = e
            break
            
    def unique(lst):
        res = []
        for x in lst:
            if not any(eq(x, y) for y in res):
                res.append(x)
        return res

    for s in S:
        found = False
        V_current = []
        if one is not None:
            for r in R:
                V_current.append(mul(r, one))
        else:
            V_current.append(zero)
            
        V_current = unique(V_current)
        
        p = s
        for n in range(1, len(S) + 2):
            if any(eq(add(p, v), zero) for v in V_current):
                found = True
                break
            
            next_V = []
            for v in V_current:
                for r in R:
                    next_V.append(add(v, mul(r, p)))
            V_current = unique(next_V)
            p = mul(p, s)
            
        if not found:
            return False
            
    return True

def check_prime_ideal(witness, Q):
    if hasattr(witness, 'is_prime_ideal'): return witness.is_prime_ideal(Q)
    if isinstance(witness, dict) and 'is_prime_ideal' in witness: return witness['is_prime_ideal'](Q)
        
    S = get_S(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    zero = get_zero(witness)
    eq = get_eq(witness)
    
    for q in Q:
        if not any(eq(q, s) for s in S): return False
        
    if not any(eq(q, zero) for q in Q): return False
    for a in Q:
        has_neg = False
        for b in Q:
            if eq(add(a, b), zero): has_neg = True
            if not any(eq(add(a, b), q) for q in Q): return False
        if not has_neg: return False
        
    for q in Q:
        for s in S:
            if not any(eq(mul(q, s), _x) for _x in Q): return False
            if not any(eq(mul(s, q), _x) for _x in Q): return False
            
    is_proper = False
    for s in S:
        if not any(eq(s, q) for q in Q):
            is_proper = True
            break
    if not is_proper: return False
    
    def generate_ideal(a):
        ideal = [a]
        for s in S:
            ideal.append(mul(s, a))
            ideal.append(mul(a, s))
            for t in S:
                ideal.append(mul(mul(s, a), t))
        
        res = []
        for _x in ideal:
            if not any(eq(_x, y) for y in res):
                res.append(_x)
        ideal = res
        
        changed = True
        while changed:
            changed = False
            new_elements = []
            for _x in ideal:
                for y in ideal:
                    s_xy = add(_x, y)
                    if not any(eq(s_xy, z) for z in ideal) and not any(eq(s_xy, z) for z in new_elements):
                        new_elements.append(s_xy)
            if new_elements:
                ideal.extend(new_elements)
                changed = True
        return ideal

    ideals = []
    for a in S:
        if not any(eq(a, q) for q in Q):
            ideals.append((a, generate_ideal(a)))
            
    for a, ideal_a in ideals:
        for b, ideal_b in ideals:
            product_in_Q = True
            for _x in ideal_a:
                for y in ideal_b:
                    xy = mul(_x, y)
                    if not any(eq(xy, q) for q in Q):
                        product_in_Q = False
                        break
                if not product_in_Q:
                    break
            if product_in_Q:
                return False
                
    return True

def check_subset(witness, sub, sup):
    if hasattr(witness, 'is_subset'): return witness.is_subset(sub, sup)
    if isinstance(witness, dict) and 'is_subset' in witness: return witness['is_subset'](sub, sup)
        
    eq = get_eq(witness)
    for x in sub:
        if not any(eq(x, y) for y in sup): return False
    return True

def check_intersection_eq(witness):
    if hasattr(witness, 'is_intersection_eq'): return witness.is_intersection_eq()
    if isinstance(witness, dict) and 'is_intersection_eq' in witness: return witness['is_intersection_eq']()
        
    R = get_R(witness)
    Q1 = get_Q1(witness)
    Q2 = get_Q2(witness)
    eq = get_eq(witness)
    
    int1 = []
    for x in Q1:
        if any(eq(x, r) for r in R):
            int1.append(x)
            
    int2 = []
    for x in Q2:
        if any(eq(x, r) for r in R):
            int2.append(x)
            
    for x in int1:
        if not any(eq(x, y) for y in int2): return False
    for x in int2:
        if not any(eq(x, y) for y in int1): return False
        
    return True

def check_neg_conclusion(witness):
    if hasattr(witness, 'is_Q1_neq_Q2'): return witness.is_Q1_neq_Q2()
    if isinstance(witness, dict) and 'is_Q1_neq_Q2' in witness: return witness['is_Q1_neq_Q2']()
        
    Q1 = get_Q1(witness)
    Q2 = get_Q2(witness)
    eq = get_eq(witness)
    
    subset12 = True
    for x in Q1:
        if not any(eq(x, y) for y in Q2):
            subset12 = False
            break
            
    subset21 = True
    for x in Q2:
        if not any(eq(x, y) for y in Q1):
            subset21 = False
            break
            
    return not (subset12 and subset21)

def conditions(witness):
    try:
        h1 = check_subring(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_integral_extension(witness)
    except Exception:
        h2 = False
        
    try:
        Q1 = get_Q1(witness)
        Q2 = get_Q2(witness)
        h3 = check_prime_ideal(witness, Q1) and check_prime_ideal(witness, Q2)
    except Exception:
        h3 = False
        
    try:
        Q1 = get_Q1(witness)
        Q2 = get_Q2(witness)
        h4 = check_subset(witness, Q1, Q2)
    except Exception:
        h4 = False
        
    try:
        h5 = check_intersection_eq(witness)
    except Exception:
        h5 = False
        
    try:
        neg_q = check_neg_conclusion(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is an integral extension of R",
    "H_3: Q_1 and Q_2 are prime ideals of S",
    "H_4: Q_1 is a subset of Q_2",
    "H_5: Q_1 ∩ R = Q_2 ∩ R",
    "¬Q: Q_1 != Q_2"
]

N_HYP = 5
NEG_Q_INDEX = 5