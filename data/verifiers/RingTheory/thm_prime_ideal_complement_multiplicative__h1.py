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

def contains(lst, item):
    return any(x == item for x in lst)

def is_ring(R):
    if not R: return False
    
    # Check closure
    for a in R:
        for b in R:
            if not contains(R, a + b): return False
            if not contains(R, a - b): return False
            if not contains(R, a * b): return False
            
    # Check addition is commutative
    for a in R:
        for b in R:
            if not (a + b == b + a): return False
            
    # Check associativity of addition
    for a in R:
        for b in R:
            ab = a + b
            for c in R:
                if not (ab + c == a + (b + c)): return False
                
    # Check associativity of multiplication
    for a in R:
        for b in R:
            ab = a * b
            for c in R:
                if not (ab * c == a * (b * c)): return False
                
    # Check distributivity
    for a in R:
        for b in R:
            ab = a * b
            for c in R:
                if not (a * (b + c) == ab + a * c): return False
                if not ((b + c) * a == b * a + c * a): return False
                
    # Check existence of zero
    has_zero = False
    for z in R:
        is_z = True
        for a in R:
            if not (a + z == a):
                is_z = False
                break
        if is_z:
            has_zero = True
            break
    if not has_zero: return False
    
    return True

def is_ideal(R, P):
    if not P: return False
    if len(P) >= len(R): return False
    
    for p in P:
        if not contains(R, p): return False
        
    for p1 in P:
        for p2 in P:
            if not contains(P, p1 + p2): return False
            if not contains(P, p1 - p2): return False
            
    for r in R:
        for p in P:
            if not contains(P, r * p): return False
            if not contains(P, p * r): return False
            
    return True

def is_prime_ideal(R, P):
    # In a general ring, an ideal P is prime if for all a, b in R:
    # a * R * b subset of P implies a in P or b in P.
    for a in R:
        for b in R:
            all_in_P = True
            for r in R:
                ar = a * r
                if not contains(P, ar * b):
                    all_in_P = False
                    break
            if all_in_P:
                if not contains(P, a) and not contains(P, b):
                    return False
    return True

def is_mult_closed(R, P):
    # R \ P is multiplicatively closed if for all a, b not in P, a * b is not in P.
    for a in R:
        if contains(P, a): continue
        for b in R:
            if contains(P, b): continue
            if contains(P, a * b):
                return False
    return True

def conditions(witness):
    try:
        R, P = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_ring(R) and is_ideal(R, P)
    except Exception:
        h1 = False
        
    try:
        prime = is_prime_ideal(R, P)
        mult_closed = is_mult_closed(R, P)
        neg_q = (prime != mult_closed)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a proper ideal of R",
    "¬Q: P is a prime ideal if and only if R \\setminus P is a multiplicatively closed subset of R fails"
]

N_HYP = 1
NEG_Q_INDEX = 1