import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(witness, name):
    if isinstance(witness, dict):
        return witness[name]
    return getattr(witness, name)

def is_ring(elements, add, mul):
    if not elements: return False
    # check closure
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
    # check add commutative
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
    # check add associative
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    # check add identity
    zero = None
    for e in elements:
        if all(add(e, a) == a and add(a, e) == a for a in elements):
            zero = e
            break
    if zero is None: return False
    # check add inverse
    for a in elements:
        if not any(add(a, b) == zero and add(b, a) == zero for b in elements): return False
    # check mul associative
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
    # check distributive
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def is_surjective_homomorphism(R_elems, R_add, R_mul, S_elems, S_add, S_mul, f):
    # check well-defined
    for a in R_elems:
        if f(a) not in S_elems: return False
    # check homomorphism
    for a in R_elems:
        for b in R_elems:
            if f(R_add(a, b)) != S_add(f(a), f(b)): return False
            if f(R_mul(a, b)) != S_mul(f(a), f(b)): return False
    # check surjective
    for s in S_elems:
        if not any(f(a) == s for a in R_elems):
            return False
    return True

def get_center(elements, mul):
    center = []
    for a in elements:
        if all(mul(a, x) == mul(x, a) for x in elements):
            center.append(a)
    return center

def conditions(witness):
    try:
        R = get_attr(witness, 'R')
        S = get_attr(witness, 'S')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        f = get_attr(witness, 'f')
    except Exception:
        return [False, False, False, False]

    # H1: f is a surjective ring homomorphism from R to S
    try:
        h1 = is_ring(R, add_R, mul_R) and is_ring(S, add_S, mul_S) and is_surjective_homomorphism(R, add_R, mul_R, S, add_S, mul_S, f)
    except Exception:
        h1 = False

    # H2: Z(S) is the center of S
    try:
        Z_S = get_center(S, mul_S)
        if hasattr(witness, 'Z_S') or (isinstance(witness, dict) and 'Z_S' in witness):
            Z_S_wit = list(get_attr(witness, 'Z_S'))
            h2 = all(x in Z_S for x in Z_S_wit) and all(x in Z_S_wit for x in Z_S)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H3: Z(R) is the center of R
    try:
        Z_R = get_center(R, mul_R)
        if hasattr(witness, 'Z_R') or (isinstance(witness, dict) and 'Z_R' in witness):
            Z_R_wit = list(get_attr(witness, 'Z_R'))
            h3 = all(x in Z_R for x in Z_R_wit) and all(x in Z_R_wit for x in Z_R)
        else:
            h3 = True
    except Exception:
        h3 = False

    # Conclusion: f^{-1}(Z(S)) is a subring of R that contains both Z(R) and ker(f)
    try:
        # find zero of S
        zero_S = None
        for s in S:
            if all(add_S(s, x) == x for x in S):
                zero_S = s
                break
        
        ker_f = [r for r in R if f(r) == zero_S]
        preimage = [r for r in R if f(r) in Z_S]
        
        # Check if preimage is a subring
        is_subring = True
        for a in preimage:
            for b in preimage:
                if add_R(a, b) not in preimage:
                    is_subring = False
                if mul_R(a, b) not in preimage:
                    is_subring = False
                    
        # find zero of R
        zero_R = None
        for r in R:
            if all(add_R(r, x) == x for x in R):
                zero_R = r
                break
                
        if zero_R not in preimage:
            is_subring = False
            
        for a in preimage:
            inv_a = None
            for x in R:
                if add_R(a, x) == zero_R and add_R(x, a) == zero_R:
                    inv_a = x
                    break
            if inv_a not in preimage:
                is_subring = False
                
        # Check if it contains Z(R)
        contains_ZR = all(r in preimage for r in Z_R)
        
        # Check if it contains ker(f)
        contains_ker = all(r in preimage for r in ker_f)
        
        Q = is_subring and contains_ZR and contains_ker
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: Z(S) is the center of S",
    "H_3: Z(R) is the center of R",
    "¬Q: f^{-1}(Z(S)) is not a subring containing Z(R) and ker(f)"
]

N_HYP = 3
NEG_Q_INDEX = 3