import sympy
from sympy import Matrix, eye, zeros
import itertools
import functools
import math

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(witness, attr, default=None):
    if isinstance(witness, dict):
        return witness.get(attr, default)
    return getattr(witness, attr, default)

def get_add(witness):
    add = get_attr(witness, 'add')
    if add: return add
    return lambda a, b: a + b

def get_mul(witness):
    mul = get_attr(witness, 'mul')
    if mul: return mul
    return lambda a, b: a * b

def get_eq(witness):
    eq = get_attr(witness, 'eq')
    if eq: return eq
    return lambda a, b: a == b

def get_zero(witness):
    zero = get_attr(witness, 'zero')
    if zero is not None: return zero
    R = get_attr(witness, 'R')
    add = get_add(witness)
    eq = get_eq(witness)
    for z in R:
        if all(eq(add(z, a), a) and eq(add(a, z), a) for a in R):
            return z
    return None

def check_H1(witness):
    S = get_attr(witness, 'S')
    mul = get_mul(witness)
    eq = get_eq(witness)
    
    if not S: 
        return False
    for a in S:
        for b in S:
            ab = mul(a, b)
            if not any(eq(ab, s) for s in S):
                return False
    return True

def check_H2(witness):
    R = get_attr(witness, 'R')
    I = get_attr(witness, 'I')
    add = get_add(witness)
    mul = get_mul(witness)
    eq = get_eq(witness)
    zero = get_zero(witness)
    
    if not I: 
        return False
    if zero is not None and not any(eq(zero, x) for x in I):
        return False
        
    for a in I:
        for b in I:
            ab = add(a, b)
            if not any(eq(ab, x) for x in I):
                return False
            # Check closure under subtraction: exists c in I such that a = b + c
            if not any(eq(a, add(b, c)) for c in I):
                return False
                
    for r in R:
        for x in I:
            rx = mul(r, x)
            xr = mul(x, r)
            if not any(eq(rx, y) for y in I): return False
            if not any(eq(xr, y) for y in I): return False
            
    return True

def check_H3(witness):
    S = get_attr(witness, 'S')
    I = get_attr(witness, 'I')
    S_prime = get_attr(witness, 'S_prime')
    add = get_add(witness)
    eq = get_eq(witness)
    
    proj = get_attr(witness, 'proj')
    if proj:
        eq_prime = get_attr(witness, 'eq_prime', eq)
        proj_S = [proj(s) for s in S]
        for sp in S_prime:
            if not any(eq_prime(sp, ps) for ps in proj_S): return False
        for ps in proj_S:
            if not any(eq_prime(sp, ps) for sp in S_prime): return False
        return True

    def same_coset(a, b):
        for x in I:
            if eq(a, add(b, x)): return True
            if eq(b, add(a, x)): return True
        return False

    if S_prime and isinstance(S_prime[0], (list, tuple, set)):
        for s in S:
            found = False
            for coset in S_prime:
                if any(same_coset(s, c) for c in coset):
                    found = True
                    break
            if not found: return False
        for coset in S_prime:
            if not any(same_coset(s, c) for s in S for c in coset):
                return False
        return True
    else:
        for s in S:
            if not any(same_coset(s, sp) for sp in S_prime):
                return False
        for sp in S_prime:
            if not any(same_coset(s, sp) for s in S):
                return False
        return True

def check_neg_Q(witness):
    R = get_attr(witness, 'R')
    S = get_attr(witness, 'S')
    mul = get_mul(witness)
    eq = get_eq(witness)
    
    # For non-commutative rings, localization exists iff S is a denominator set (Ore condition).
    # If Ore condition fails, the localized ring does not exist, hence the conclusion fails.
    left_ore = True
    for r in R:
        for s in S:
            found = False
            for r_prime in R:
                for s_prime in S:
                    if eq(mul(s_prime, r), mul(r_prime, s)):
                        found = True
                        break
                if found: break
            if not found:
                left_ore = False
                break
        if not left_ore: break
        
    if not left_ore:
        return True
        
    right_ore = True
    for r in R:
        for s in S:
            found = False
            for r_prime in R:
                for s_prime in S:
                    if eq(mul(r, s_prime), mul(s, r_prime)):
                        found = True
                        break
                if found: break
            if not found:
                right_ore = False
                break
        if not right_ore: break

    return not right_ore

def conditions(witness):
    try:
        h1 = bool(check_H1(witness))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_H2(witness))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_H3(witness))
    except Exception:
        h3 = False

    try:
        neg_q = bool(check_neg_Q(witness))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is an ideal of R",
    "H_3: S' is the image of S under the canonical projection from R to R/I",
    "¬Q: The localized quotient ring (S^{-1}R)/(S^{-1}I) is not isomorphic to (S')^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3