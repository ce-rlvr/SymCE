import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: Q is a primary ideal if and only if Q is a maximal ideal (fails)"
]
N_HYP = 1
NEG_Q_INDEX = 1

def get_zero(R):
    for e in R:
        if all((e + x) == x for x in R) and all((x + e) == x for x in R):
            return e
    return None

def is_Boolean_ring(R):
    try:
        R = list(R)
        if not R: return False
        zero = get_zero(R)
        if zero is None: return False
        
        for x in R:
            for y in R:
                if (x + y) not in R: return False
                if (x * y) not in R: return False
                
        for x in R:
            for y in R:
                if (x + y) != (y + x): return False
                
        for x in R:
            for y in R:
                for z in R:
                    if ((x + y) + z) != (x + (y + z)): return False
                    if ((x * y) * z) != (x * (y * z)): return False
                    if (x * (y + z)) != ((x * y) + (x * z)): return False
                    if ((y + z) * x) != ((y * x) + (z * x)): return False
                    
        for x in R:
            has_inv = False
            for y in R:
                if (x + y) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for x in R:
            if (x * x) != x: return False
            
        return True
    except Exception:
        return False

def is_ideal(R, Q):
    try:
        zero = get_zero(R)
        if zero not in Q: return False
        for q1 in Q:
            for q2 in Q:
                if (q1 + q2) not in Q: return False
        for q in Q:
            has_inv = False
            for x in R:
                if (q + x) == zero:
                    if x not in Q: return False
                    has_inv = True
                    break
            if not has_inv: return False
        for q in Q:
            for r in R:
                if (r * q) not in Q: return False
                if (q * r) not in Q: return False
        return True
    except Exception:
        return False

def is_primary(R, Q):
    try:
        if len(Q) == len(R): return False
        for x in R:
            for y in R:
                if (x * y) in Q:
                    if x in Q: continue
                    yn = y
                    found = False
                    for _ in range(len(R) + 1):
                        if yn in Q:
                            found = True
                            break
                        yn = yn * y
                    if not found:
                        return False
        return True
    except Exception:
        return False

def is_maximal(R, Q, all_ideals):
    try:
        if len(Q) == len(R): return False
        for I in all_ideals:
            if len(Q) < len(I) < len(R):
                if all(q in I for q in Q):
                    return False
        return True
    except Exception:
        return False

def get_all_ideals(R):
    ideals = []
    zero = get_zero(R)
    if zero is None: return []
    
    def closure(S):
        cl = list(S)
        if zero not in cl: cl.append(zero)
        changed = True
        while changed:
            changed = False
            new_elements = []
            for a in cl:
                for b in cl:
                    if (a + b) not in cl and (a + b) not in new_elements:
                        new_elements.append(a + b)
                for r in R:
                    if (r * a) not in cl and (r * a) not in new_elements:
                        new_elements.append(r * a)
                    if (a * r) not in cl and (a * r) not in new_elements:
                        new_elements.append(a * r)
            if new_elements:
                cl.extend(new_elements)
                changed = True
        # Sort by string representation to allow list comparison
        return sorted(cl, key=lambda x: str(x))

    base_ideals = []
    for x in R:
        base_ideals.append(closure([x]))
        
    current_ideals = list(base_ideals)
    all_found = []
    
    while current_ideals:
        next_ideals = []
        for I in current_ideals:
            if I not in all_found:
                all_found.append(I)
                for J in base_ideals:
                    sum_IJ = closure(I + J)
                    if sum_IJ not in all_found and sum_IJ not in next_ideals:
                        next_ideals.append(sum_IJ)
        current_ideals = next_ideals
        
    return all_found

def conditions(witness):
    try:
        is_tuple = isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, set, tuple))
        if is_tuple:
            R = list(witness[0])
            Q_target = list(witness[1])
        else:
            R = list(witness)
            Q_target = None
            
        if len(R) > 64:
            return [False, False]
            
        h1 = is_Boolean_ring(R)
        if not h1:
            return [False, False]
            
        all_ideals = get_all_ideals(R)
        
        if Q_target is not None:
            if not is_ideal(R, Q_target):
                return [True, False]
            prim = is_primary(R, Q_target)
            maxi = is_maximal(R, Q_target, all_ideals)
            neg_q = (prim != maxi)
            return [True, neg_q]
        else:
            neg_q = False
            for Q in all_ideals:
                prim = is_primary(R, Q)
                maxi = is_maximal(R, Q, all_ideals)
                if prim != maxi:
                    neg_q = True
                    break
            return [True, neg_q]
            
    except Exception:
        return [False, False]