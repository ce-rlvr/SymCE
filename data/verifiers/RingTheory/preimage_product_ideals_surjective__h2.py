import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools

# Top-level setup
# (No specific named objects required for this general ring theory verifier)

def is_ring(elements, add_op, mul_op, zero, one):
    elements = set(elements)
    if zero not in elements or one not in elements:
        return False
        
    # Check closure and commutativity of addition
    for a in elements:
        if add_op(a, zero) != a: return False
        if add_op(zero, a) != a: return False
        if mul_op(a, one) != a: return False
        if mul_op(one, a) != a: return False
        
        has_inv = False
        for b in elements:
            ab_add = add_op(a, b)
            if ab_add not in elements: return False
            if mul_op(a, b) not in elements: return False
            if ab_add != add_op(b, a): return False
            if ab_add == zero:
                has_inv = True
        if not has_inv: return False

    # Check associativity and distributivity
    for a in elements:
        for b in elements:
            ab_add = add_op(a, b)
            ab_mul = mul_op(a, b)
            for c in elements:
                if add_op(ab_add, c) != add_op(a, add_op(b, c)): return False
                if mul_op(ab_mul, c) != mul_op(a, mul_op(b, c)): return False
                if mul_op(a, add_op(b, c)) != add_op(ab_mul, mul_op(a, c)): return False
                if mul_op(ab_add, c) != add_op(mul_op(a, c), mul_op(b, c)): return False
                
    return True

def is_homomorphism(f, R, S, add_R, mul_R, add_S, mul_S, one_R, one_S):
    R = set(R)
    S = set(S)
    if f(one_R) != one_S: return False
    for a in R:
        fa = f(a)
        if fa not in S: return False
        for b in R:
            if f(add_R(a, b)) != add_S(fa, f(b)): return False
            if f(mul_R(a, b)) != mul_S(fa, f(b)): return False
    return True

def is_ideal(I, S, add_S, mul_S, zero_S):
    I = set(I)
    S = set(S)
    if not I: return False
    if not I.issubset(S): return False
    if zero_S not in I: return False
    for a in I:
        has_inv = False
        for b in I:
            if add_S(a, b) == zero_S:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in I:
            if add_S(a, b) not in I: return False
        for r in S:
            if mul_S(a, r) not in I: return False
            if mul_S(r, a) not in I: return False
    return True

def additive_closure(elements, add_op, zero):
    closure = set(elements)
    closure.add(zero)
    queue = list(closure)
    
    while queue:
        a = queue.pop(0)
        new_elements = set()
        for b in closure:
            c = add_op(a, b)
            if c not in closure and c not in new_elements:
                new_elements.add(c)
            c2 = add_op(b, a)
            if c2 not in closure and c2 not in new_elements:
                new_elements.add(c2)
        for c in new_elements:
            closure.add(c)
            queue.append(c)
            
    return closure

def conditions(witness) -> list[bool]:
    try:
        R = set(witness['R'])
        S = set(witness['S'])
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        zero_R = witness['zero_R']
        one_R = witness['one_R']
        
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_S = witness['zero_S']
        one_S = witness['one_S']
        
        I = set(witness['I'])
        J = set(witness['J'])
        f = witness['f']
        
        h1 = is_ring(R, add_R, mul_R, zero_R, one_R) and \
             is_ring(S, add_S, mul_S, zero_S, one_S) and \
             is_homomorphism(f, R, S, add_R, mul_R, add_S, mul_S, one_R, one_S)
             
        h2 = is_ideal(I, S, add_S, mul_S, zero_S) and \
             is_ideal(J, S, add_S, mul_S, zero_S)
             
        IJ_prods = {mul_S(a, b) for a in I for b in J}
        IJ = additive_closure(IJ_prods, add_S, zero_S)
        
        f_inv_IJ = {x for x in R if f(x) in IJ}
        
        f_inv_I = {x for x in R if f(x) in I}
        f_inv_J = {x for x in R if f(x) in J}
        
        f_inv_I_f_inv_J_prods = {mul_R(x, y) for x in f_inv_I for y in f_inv_J}
        f_inv_I_f_inv_J = additive_closure(f_inv_I_f_inv_J_prods, add_R, zero_R)
        
        ker_f = {x for x in R if f(x) == zero_S}
        
        sum_ideal = {add_R(u, v) for u in f_inv_I_f_inv_J for v in ker_f}
        
        neg_q = (f_inv_IJ != sum_ideal)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings and f is a ring homomorphism from R to S",
    "H_2: I and J are ideals of S",
    "¬Q: f^{-1}(IJ) != f^{-1}(I)f^{-1}(J) + ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2