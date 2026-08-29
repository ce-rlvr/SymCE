import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def unique_elements(lst):
    res = []
    for x in lst:
        if x not in res:
            res.append(x)
    return res

def is_subset(sub, sup):
    return all(x in sup for x in sub)

def set_equal(lst1, lst2):
    return is_subset(lst1, lst2) and is_subset(lst2, lst1)

def check_finite_ring(R, add, mul, I_el, Qs_el):
    R_list = unique_elements(R)
    
    def is_ideal(S):
        S_list = unique_elements(S)
        if not is_subset(S_list, R_list): return False
        if not S_list: return False
        for a in S_list:
            for b in S_list:
                if add(a, b) not in S_list: return False
        for a in S_list:
            for r in R_list:
                if mul(a, r) not in S_list: return False
                if mul(r, a) not in S_list: return False
        return True

    h1 = is_ideal(I_el) and not set_equal(I_el, R_list)
    
    intersect = R_list
    for Q in Qs_el:
        intersect = [x for x in intersect if x in Q]
    h2_intersect = set_equal(I_el, intersect)
    
    h2_primary = True
    for Q in Qs_el:
        if not is_ideal(Q):
            h2_primary = False
            break
        is_prim = True
        for a in R_list:
            for b in R_list:
                if mul(a, b) in Q:
                    if a not in Q:
                        b_pow = b
                        found = False
                        for m in range(1, len(R_list) + 2):
                            if b_pow in Q:
                                found = True
                                break
                            b_pow = mul(b_pow, b)
                        if not found:
                            is_prim = False
                            break
            if not is_prim:
                break
        if not is_prim:
            h2_primary = False
            break
            
    h2 = h2_intersect and h2_primary
    
    def radical(S):
        rad = []
        for x in R_list:
            x_pow = x
            for m in range(1, len(R_list) + 2):
                if x_pow in S:
                    if x not in rad:
                        rad.append(x)
                    break
                x_pow = mul(x_pow, x)
        return rad
        
    def is_prime(S):
        if set_equal(S, R_list): return False
        if not is_ideal(S): return False
        for a in R_list:
            for b in R_list:
                if mul(a, b) in S:
                    if a not in S and b not in S:
                        return False
        return True

    rad_I = radical(I_el)
    intersect_rad_Q = R_list
    all_rad_Q_are_prime = True
    for Q in Qs_el:
        rad_Q = radical(Q)
        if not is_prime(rad_Q):
            all_rad_Q_are_prime = False
        intersect_rad_Q = [x for x in intersect_rad_Q if x in rad_Q]
        
    conclusion_holds = all_rad_Q_are_prime and set_equal(rad_I, intersect_rad_Q)
    neg_q = not conclusion_holds
    
    return [h1, h2, neg_q]

def conditions(witness):
    # 1. Try custom object with methods
    try:
        if hasattr(witness, 'is_proper_ideal'):
            h1 = witness.is_proper_ideal()
            h2 = witness.is_primary_decomposition()
            neg_q = not witness.conclusion_holds()
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Try dictionary format
    try:
        if isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            I_el = witness['I']
            Qs_el = witness['Qs']
            return check_finite_ring(R, add, mul, I_el, Qs_el)
    except Exception:
        pass

    # 3. Try tuple format (R, add, mul, I, Qs)
    try:
        if isinstance(witness, tuple) and len(witness) == 5 and callable(witness[1]):
            R, add, mul, I_el, Qs_el = witness
            return check_finite_ring(R, add, mul, I_el, Qs_el)
    except Exception:
        pass

    # 4. Try tuple format (n, k, I_el, Qs_el) for subrings of Z_n
    try:
        if isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], int):
            n, k, I_el, Qs_el = witness
            R = [x for x in range(n) if x % k == 0]
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            return check_finite_ring(R, add, mul, I_el, Qs_el)
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: I = ∩_{i=1}^n Q_i is a primary decomposition of I",
    "¬Q: The radical √I is not equal to the intersection of the prime ideals √Q_i (or some √Q_i is not prime)"
]

N_HYP = 2
NEG_Q_INDEX = 2