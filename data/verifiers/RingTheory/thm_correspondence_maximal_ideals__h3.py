import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_ring_info(R):
    if isinstance(R, int):
        if R <= 0:
            raise ValueError("n must be positive")
        n = R
        elements = list(range(n))
        add = lambda x, y: (x + y) % n
        mul = lambda x, y: (x * y) % n
        zero = 0
        one = 1 % n if n > 1 else 0
        return elements, add, mul, zero, one
    elif isinstance(R, tuple) and len(R) == 5:
        return R
    else:
        elements = list(R.elements)
        add = R.add
        mul = R.mul
        zero = R.zero
        one = getattr(R, 'one', None)
        if one is None:
            for e in elements:
                if all(mul(e, x) == x and mul(x, e) == x for x in elements):
                    one = e
                    break
        return elements, add, mul, zero, one

def is_commutative(R_info):
    elements, add, mul, zero, one = R_info
    for x in elements:
        for y in elements:
            if mul(x, y) != mul(y, x):
                return False
    return True

def has_identity(R_info):
    elements, add, mul, zero, one = R_info
    if one is None:
        return False
    for x in elements:
        if mul(one, x) != x or mul(x, one) != x:
            return False
    return True

def get_ideal_elements(I, R_info):
    elements, add, mul, zero, one = R_info
    if isinstance(I, int):
        ideal = set()
        for x in elements:
            ideal.add(mul(I, x))
        return list(ideal)
    elif isinstance(I, (list, set, frozenset, tuple)):
        return list(I)
    else:
        return list(I.elements)

def is_proper_ideal(I_elements, R_info):
    elements, add, mul, zero, one = R_info
    I_set = set(I_elements)
    if len(I_set) == len(elements):
        return False
    if zero not in I_set:
        return False
    for x in I_set:
        for y in I_set:
            if add(x, y) not in I_set:
                return False
    for x in I_set:
        neg_x = None
        for y in elements:
            if add(x, y) == zero:
                neg_x = y
                break
        if neg_x not in I_set:
            return False
    for x in I_set:
        for r in elements:
            if mul(r, x) not in I_set:
                return False
            if mul(x, r) not in I_set:
                return False
    return True

def get_all_ideals(R_info):
    elements, add, mul, zero, one = R_info
    
    def get_ideal_generated_by(subset):
        closure = set(subset)
        if zero not in closure:
            closure.add(zero)
        while True:
            new_elements = set()
            for x in closure:
                for r in elements:
                    rx = mul(r, x)
                    xr = mul(x, r)
                    if rx not in closure: new_elements.add(rx)
                    if xr not in closure: new_elements.add(xr)
            for x in closure:
                for y in closure:
                    xy = add(x, y)
                    if xy not in closure: new_elements.add(xy)
            if not new_elements:
                break
            closure.update(new_elements)
        return frozenset(closure)

    principal_ideals = set()
    for x in elements:
        principal_ideals.add(get_ideal_generated_by({x}))
        
    ideals = set(principal_ideals)
    new_ideals = set(principal_ideals)
    while new_ideals:
        next_new = set()
        for I1 in new_ideals:
            for I2 in principal_ideals:
                sum_ideal = set()
                for x in I1:
                    for y in I2:
                        sum_ideal.add(add(x, y))
                sum_ideal = frozenset(sum_ideal)
                if sum_ideal not in ideals:
                    ideals.add(sum_ideal)
                    next_new.add(sum_ideal)
        new_ideals = next_new
    return ideals

def get_maximal_ideals(R_info):
    elements, add, mul, zero, one = R_info
    ideals = get_all_ideals(R_info)
    proper_ideals = [I for I in ideals if len(I) < len(elements)]
    max_ideals = []
    for I in proper_ideals:
        is_max = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_max = False
                break
        if is_max:
            max_ideals.append(I)
    return max_ideals

def get_quotient_ring(R_info, I_elements):
    elements, add, mul, zero, one = R_info
    I_set = frozenset(I_elements)
    cosets = set()
    for x in elements:
        coset = frozenset(add(x, i) for i in I_set)
        cosets.add(coset)
    cosets = list(cosets)
    
    def coset_add(c1, c2):
        x = next(iter(c1))
        y = next(iter(c2))
        sum_xy = add(x, y)
        for c in cosets:
            if sum_xy in c:
                return c
                
    def coset_mul(c1, c2):
        x = next(iter(c1))
        y = next(iter(c2))
        prod_xy = mul(x, y)
        for c in cosets:
            if prod_xy in c:
                return c
                
    zero_coset = None
    for c in cosets:
        if zero in c:
            zero_coset = c
            break
            
    one_coset = None
    if one is not None:
        for c in cosets:
            if one in c:
                one_coset = c
                break
            
    return cosets, coset_add, coset_mul, zero_coset, one_coset

def check_bijection(R_info, I_elements):
    elements, add, mul, zero, one = R_info
    I_set = frozenset(I_elements)
    
    max_ideals_R = get_maximal_ideals(R_info)
    max_ideals_R_I = [M for M in max_ideals_R if I_set.issubset(M)]
    
    quotient_info = get_quotient_ring(R_info, I_elements)
    max_ideals_quotient = get_maximal_ideals(quotient_info)
    
    pi_M_list = []
    for M in max_ideals_R_I:
        pi_M = set()
        for x in M:
            for c in quotient_info[0]:
                if x in c:
                    pi_M.add(c)
                    break
        pi_M_list.append(frozenset(pi_M))
        
    set_pi_M = set(pi_M_list)
    set_max_quotient = set(max_ideals_quotient)
    
    if len(set_pi_M) != len(max_ideals_R_I):
        return False
        
    return set_pi_M == set_max_quotient

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
        
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        R_info = get_ring_info(R)
        h1 = is_commutative(R_info) and has_identity(R_info)
        I_elements = get_ideal_elements(I, R_info)
        h2 = is_proper_ideal(I_elements, R_info)
        
        if h1 and h2:
            bijection = check_bijection(R_info, I_elements)
            neg_q = not bijection
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: The map M \\mapsto \\pi(M) does not establish a bijection between the maximal ideals of R containing I and the maximal ideals of R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2