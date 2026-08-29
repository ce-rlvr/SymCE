import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def get_val(op, a, b=None):
    if b is None:
        if isinstance(op, dict): return op[a]
        return op(a)
    if isinstance(op, dict): return op[(a, b)]
    return op(a, b)

def get_zero(elements, add):
    for e in elements:
        if all(get_val(add, e, x) == x for x in elements):
            return e
    return None

def is_ring(elements, add, mul):
    if not elements: return False
    zero = get_zero(elements, add)
    if zero is None: return False
    
    for a in elements:
        if not any(get_val(add, a, b) == zero and get_val(add, b, a) == zero for b in elements):
            return False
        for b in elements:
            if get_val(add, a, b) not in elements: return False
            if get_val(mul, a, b) not in elements: return False
            if get_val(add, a, b) != get_val(add, b, a): return False
            for c in elements:
                if get_val(add, get_val(add, a, b), c) != get_val(add, a, get_val(add, b, c)): return False
                if get_val(mul, get_val(mul, a, b), c) != get_val(mul, a, get_val(mul, b, c)): return False
                if get_val(mul, a, get_val(add, b, c)) != get_val(add, get_val(mul, a, b), get_val(mul, a, c)): return False
                if get_val(mul, get_val(add, a, b), c) != get_val(add, get_val(mul, a, c), get_val(mul, b, c)): return False
    return True

def get_all_ideals(elements, add, mul, zero):
    inverses = {}
    for a in elements:
        for b in elements:
            if get_val(add, a, b) == zero:
                inverses[a] = b
                break

    def generate_ideal(generators):
        closure = set(generators)
        closure.add(zero)
        changed = True
        while changed:
            changed = False
            new_elements = set()
            for a in closure:
                if inverses[a] not in closure:
                    new_elements.add(inverses[a])
                for b in closure:
                    c = get_val(add, a, b)
                    if c not in closure:
                        new_elements.add(c)
                for r in elements:
                    c1 = get_val(mul, r, a)
                    c2 = get_val(mul, a, r)
                    if c1 not in closure: new_elements.add(c1)
                    if c2 not in closure: new_elements.add(c2)
            if new_elements:
                closure.update(new_elements)
                changed = True
        return frozenset(closure)

    ideals = set()
    ideals.add(generate_ideal([]))
    
    queue = list(ideals)
    while queue:
        current = queue.pop(0)
        for x in elements:
            if x not in current:
                new_ideal = generate_ideal(list(current) + [x])
                if new_ideal not in ideals:
                    ideals.add(new_ideal)
                    queue.append(new_ideal)
                    
    return [set(I) for I in ideals]

def conditions(witness):
    try:
        R_elements = witness['R_elements']
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        S_elements = witness['S_elements']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        f = witness['f']
        K = witness['K']
    except Exception:
        return [False, False, False]

    try:
        h1 = is_ring(R_elements, add_R, mul_R) and is_ring(S_elements, add_S, mul_S)
    except Exception:
        h1 = False

    try:
        zero_S = get_zero(S_elements, add_S)
        is_hom = True
        for a in R_elements:
            for b in R_elements:
                if get_val(f, get_val(add_R, a, b)) != get_val(add_S, get_val(f, a), get_val(f, b)):
                    is_hom = False
                if get_val(f, get_val(mul_R, a, b)) != get_val(mul_S, get_val(f, a), get_val(f, b)):
                    is_hom = False
        
        actual_K = set(x for x in R_elements if get_val(f, x) == zero_S)
        h2 = is_hom and set(K) == actual_K
    except Exception:
        h2 = False

    try:
        zero_R = get_zero(R_elements, add_R)
        zero_S = get_zero(S_elements, add_S)
        if zero_R is None or zero_S is None:
            neg_q = False
        else:
            ideals_R = get_all_ideals(R_elements, add_R, mul_R, zero_R)
            K_set = set(K)
            ideals_R_containing_K = [I for I in ideals_R if K_set.issubset(I)]
            
            ideals_S = get_all_ideals(S_elements, add_S, mul_S, zero_S)
            
            is_bijection = True
            mapped_ideals = []
            
            for I in ideals_R_containing_K:
                f_I = set(get_val(f, x) for x in I)
                if f_I not in ideals_S:
                    is_bijection = False
                    break
                mapped_ideals.append(f_I)
                
            if is_bijection:
                unique_mapped = []
                for m in mapped_ideals:
                    if m not in unique_mapped:
                        unique_mapped.append(m)
                if len(unique_mapped) != len(ideals_R_containing_K):
                    is_bijection = False
                    
            if is_bijection:
                for J in ideals_S:
                    if J not in mapped_ideals:
                        is_bijection = False
                        break
                        
            neg_q = not is_bijection
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: K is the kernel of f",
    "¬Q: The map I -> f(I) is not a bijection from ideals of R containing K to ideals of S"
]

N_HYP = 2
NEG_Q_INDEX = 2