import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_eq(a, b):
    try:
        res = (a == b)
        if isinstance(res, bool):
            return res
        return bool(res.all())
    except Exception:
        return False

def is_in(x, lst):
    return any(is_eq(x, y) for y in lst)

def conditions(witness):
    try:
        R, I = witness
        R = list(R)
        I = list(I)
    except Exception:
        return [False, False, False]
        
    # H1: R is a right Artinian ring
    # We check if R is a finite ring (which implies Artinian).
    # Note: We do not enforce associativity of multiplication, as the dropped hypothesis
    # from the true theorem is that the ring is associative (e.g. counterexamples are Lie algebras).
    try:
        h1 = True
        if not R:
            h1 = False
        else:
            # closure
            for a in R:
                for b in R:
                    if not is_in(a + b, R): h1 = False
                    if not is_in(a * b, R): h1 = False
                    if not is_eq(a + b, b + a): h1 = False
            
            # associativity of + and distributivity
            for a in R:
                for b in R:
                    for c in R:
                        if not is_eq((a + b) + c, a + (b + c)): h1 = False
                        if not is_eq(a * (b + c), a * b + a * c): h1 = False
                        if not is_eq((a + b) * c, a * c + b * c): h1 = False
                        
            # zero element
            zero = None
            for z in R:
                if all(is_eq(z + a, a) for a in R):
                    zero = z
                    break
            if zero is None:
                h1 = False
            else:
                # additive inverses
                for a in R:
                    if not any(is_eq(a + b, zero) for b in R): h1 = False
    except Exception:
        h1 = False

    # H2: I is not a nilpotent ideal
    try:
        h2 = False
        if h1 and I:
            # check if I is an ideal
            is_id = True
            for x in I:
                if not is_in(x, R): is_id = False
            for a in I:
                for b in I:
                    if not is_in(a + b, I): is_id = False
            for r in R:
                for x in I:
                    if not is_in(r * x, I): is_id = False
                    if not is_in(x * r, I): is_id = False
                    
            if is_id:
                I_unique = []
                for x in I:
                    if not is_in(x, I_unique):
                        I_unique.append(x)
                        
                curr_power = I_unique
                seen = []
                is_nilp = False
                
                while True:
                    if all(is_eq(x, zero) for x in curr_power):
                        is_nilp = True
                        break
                        
                    # check cycle
                    cycled = False
                    for s in seen:
                        if len(s) == len(curr_power) and all(is_in(x, s) for x in curr_power):
                            cycled = True
                            break
                    if cycled:
                        is_nilp = False
                        break
                        
                    seen.append(list(curr_power))
                    
                    prods = []
                    for a in I:
                        for b in curr_power:
                            p = a * b
                            if not is_in(p, prods):
                                prods.append(p)
                                
                    next_power = []
                    q = []
                    for p in prods:
                        next_power.append(p)
                        q.append(p)
                        
                    if not is_in(zero, next_power):
                        next_power.append(zero)
                        q.append(zero)
                        
                    while q:
                        curr = q.pop(0)
                        for p in prods:
                            nxt = curr + p
                            if not is_in(nxt, next_power):
                                next_power.append(nxt)
                                q.append(nxt)
                                
                    curr_power = next_power
                    
                h2 = not is_nilp
    except Exception:
        h2 = False

    # neg_Q: I does not contain a non-zero idempotent element
    try:
        neg_q = True
        if h1:
            for x in I:
                if not is_eq(x, zero) and is_eq(x * x, x):
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: I is not a nilpotent ideal",
    "¬Q: I does not contain a non-zero idempotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2