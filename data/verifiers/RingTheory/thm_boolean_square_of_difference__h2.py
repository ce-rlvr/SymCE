import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def is_eq(val1, val2):
    try:
        return bool(val1 == val2)
    except Exception:
        return False

def contains(lst, val):
    for item in lst:
        if is_eq(item, val):
            return True
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, x, y), checks if R is a Boolean ring and if (x - y)^2 != x + y.
    """
    try:
        R, x, y = witness
    except Exception:
        return [False, False]
        
    h1 = False
    try:
        R_iterator = iter(R)
        R_list = []
        # Limit to 64 elements to ensure fast execution (64^3 is ~2.6e5 iterations)
        for _ in range(65):
            try:
                R_list.append(next(R_iterator))
            except StopIteration:
                break
                
        if 0 < len(R_list) <= 64:
            is_ring = True
            
            # Check closure, commutativity of addition, valid subtraction, and idempotence
            for a in R_list:
                if not is_ring: break
                if not is_eq(a * a, a):
                    is_ring = False
                    break
                for b in R_list:
                    if not contains(R_list, a + b): is_ring = False; break
                    if not contains(R_list, a * b): is_ring = False; break
                    if not contains(R_list, a - b): is_ring = False; break
                    if not is_eq(a + b, b + a): is_ring = False; break
                    if not is_eq((a - b) + b, a): is_ring = False; break
                    
            # Check associativity and distributivity
            if is_ring:
                for a in R_list:
                    if not is_ring: break
                    for b in R_list:
                        if not is_ring: break
                        for c in R_list:
                            if not is_eq((a + b) + c, a + (b + c)): is_ring = False; break
                            if not is_eq((a * b) * c, a * (b * c)): is_ring = False; break
                            if not is_eq(a * (b + c), (a * b) + (a * c)): is_ring = False; break
                            if not is_eq((a + b) * c, (a * c) + (b * c)): is_ring = False; break
                            
            # Check existence of additive identity
            if is_ring:
                has_zero = False
                for z in R_list:
                    if all(is_eq(a + z, a) for a in R_list):
                        has_zero = True
                        break
                if has_zero:
                    h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        # The conclusion is (x - y)^2 = x + y.
        # We check if it fails (i.e., they are not equal).
        if not is_eq((x - y) * (x - y), x + y):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: (x - y)^2 != x + y"
]

N_HYP = 1
NEG_Q_INDEX = 1