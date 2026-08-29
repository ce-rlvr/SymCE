import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def is_in(element, lst):
    return any(eq(element, x) for x in lst)

def get_zero(elements, add):
    for e in elements:
        if all(eq(add(e, a), a) and eq(add(a, e), a) for a in elements):
            return e
    return None

def get_neg(elements, add, zero):
    neg = {}
    for i, a in enumerate(elements):
        for b in elements:
            if eq(add(a, b), zero) and eq(add(b, a), zero):
                neg[i] = b
                break
    return neg

def get_identity(elements, mul):
    for e in elements:
        if all(eq(mul(e, a), a) and eq(mul(a, e), a) for a in elements):
            return e
    return None

def get_closure(X, elements, add, mul, zero, neg, unital, one):
    closure = []
    for x in X:
        if not is_in(x, closure):
            closure.append(x)
            
    if unital and one is not None:
        if not is_in(one, closure):
            closure.append(one)
            
    if not closure and zero is not None:
        closure.append(zero)
        
    added = True
    while added:
        added = False
        new_elements = []
        for a in closure:
            idx = -1
            for i, e in enumerate(elements):
                if eq(e, a):
                    idx = i
                    break
            if idx != -1 and idx in neg:
                n_a = neg[idx]
                if not is_in(n_a, closure) and not is_in(n_a, new_elements):
                    new_elements.append(n_a)
                    
            for b in closure:
                s = add(a, b)
                if not is_in(s, closure) and not is_in(s, new_elements):
                    new_elements.append(s)
                p = mul(a, b)
                if not is_in(p, closure) and not is_in(p, new_elements):
                    new_elements.append(p)
                    
        if new_elements:
            closure.extend(new_elements)
            added = True
            
    return closure

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            f = witness['f']
            X = witness['X']
            unital = witness.get('unital', False)
        else:
            R = witness.R
            S = witness.S
            add_R = witness.add_R
            mul_R = witness.mul_R
            add_S = witness.add_S
            mul_S = witness.mul_S
            f = witness.f
            X = witness.X
            unital = getattr(witness, 'unital', False)
    except Exception:
        return [False, False, False]
        
    # H1: f is a surjective ring homomorphism from R to S
    try:
        h1 = True
        f_R = []
        for r in R:
            fr = f(r)
            if not is_in(fr, f_R):
                f_R.append(fr)
                
        for s in S:
            if not is_in(s, f_R):
                h1 = False
                break
        for fr in f_R:
            if not is_in(fr, S):
                h1 = False
                break
                
        if h1:
            for a in R:
                for b in R:
                    if not eq(f(add_R(a, b)), add_S(f(a), f(b))):
                        h1 = False
                    if not eq(f(mul_R(a, b)), mul_S(f(a), f(b))):
                        h1 = False
    except Exception:
        h1 = False
        
    # H2: X is a subset of R that generates R as a ring
    try:
        zero_R = get_zero(R, add_R)
        neg_R = get_neg(R, add_R, zero_R)
        one_R = get_identity(R, mul_R) if unital else None
        
        closure_R = get_closure(X, R, add_R, mul_R, zero_R, neg_R, unital, one_R)
        
        h2 = True
        for r in R:
            if not is_in(r, closure_R):
                h2 = False
                break
        for c in closure_R:
            if not is_in(c, R):
                h2 = False
                break
        for x in X:
            if not is_in(x, R):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # Neg Q: The image f(X) does NOT generate S as a ring
    try:
        zero_S = get_zero(S, add_S)
        neg_S = get_neg(S, add_S, zero_S)
        one_S = get_identity(S, mul_S) if unital else None
        
        f_X = [f(x) for x in X]
        closure_S = get_closure(f_X, S, add_S, mul_S, zero_S, neg_S, unital, one_S)
        
        neg_q = False
        for s in S:
            if not is_in(s, closure_S):
                neg_q = True
                break
        for c in closure_S:
            if not is_in(c, S):
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: X is a subset of R that generates R as a ring",
    "¬Q: The image f(X) does not generate S as a ring"
]

N_HYP = 2
NEG_Q_INDEX = 2