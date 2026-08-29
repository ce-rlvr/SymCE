import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
# Witness is expected to be a dictionary with keys:
# 'elements': list of elements
# 'add': callable f(a, b) or dict mapping (a, b) -> c
# 'mul': callable f(a, b) or dict mapping (a, b) -> c
# 'zero': the zero element
# 'I': list of elements in subset I
# 'J': list of elements in subset J

def make_Zn(n):
    return {
        'elements': list(range(n)),
        'add': lambda a, b: (a + b) % n,
        'mul': lambda a, b: (a * b) % n,
        'zero': 0
    }

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)
Z8 = make_Zn(8)

# A commutative ring without identity: 2Z / 8Z
R_2Z_8Z = {
    'elements': [0, 2, 4, 6],
    'add': lambda a, b: (a + b) % 8,
    'mul': lambda a, b: (a * b) % 8,
    'zero': 0
}

def is_ideal(elements, add, mul, zero, I_list):
    I_set = set(I_list)
    if zero not in I_set: 
        return False
    for a in I_set:
        for b in I_set:
            if add(a, b) not in I_set: 
                return False
    for a in I_set:
        inv_a = None
        for x in elements:
            if add(a, x) == zero:
                inv_a = x
                break
        if inv_a not in I_set: 
            return False
    for a in I_set:
        for r in elements:
            if mul(a, r) not in I_set: return False
            if mul(r, a) not in I_set: return False
    return True

def is_commutative_ring(elements, add, mul, zero):
    if zero not in elements: 
        return False
    n = len(elements)
    if n == 0: 
        return False
    
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    for a in elements:
        if add(a, zero) != a: return False
        
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def get_nilradical(elements, mul, zero):
    nil = []
    for a in elements:
        curr = a
        is_nil = False
        for _ in range(len(elements)):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, a)
        if is_nil:
            nil.append(a)
    return nil

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add_func = witness['add']
            mul_func = witness['mul']
            zero = witness['zero']
            I = witness['I']
            J = witness['J']
        elif isinstance(witness, tuple) and len(witness) == 6:
            elements, add_func, mul_func, zero, I, J = witness
        else:
            return [False, False, False, False]
            
        if isinstance(add_func, dict):
            add = lambda a, b: add_func[(a, b)]
        else:
            add = add_func
            
        if isinstance(mul_func, dict):
            mul = lambda a, b: mul_func[(a, b)]
        else:
            mul = mul_func
            
        elements = list(elements)
        I = list(I)
        J = list(J)
        
        # H1: R is a commutative ring
        h1 = is_commutative_ring(elements, add, mul, zero)
        if not h1:
            return [False, False, False, False]
            
        # H2: Nil(R) is the nilradical of R
        nil = get_nilradical(elements, mul, zero)
        h2 = True
        
        # H3: The image of I and the image of J in the quotient ring R/Nil(R) are comaximal
        I_plus_nil = set()
        for i in I:
            for n in nil:
                I_plus_nil.add(add(i, n))
                
        J_plus_nil = set()
        for j in J:
            for n in nil:
                J_plus_nil.add(add(j, n))
                
        is_I_img_ideal = is_ideal(elements, add, mul, zero, list(I_plus_nil))
        is_J_img_ideal = is_ideal(elements, add, mul, zero, list(J_plus_nil))
        
        sum_IJ_nil = set()
        for x in I_plus_nil:
            for y in J_plus_nil:
                sum_IJ_nil.add(add(x, y))
                
        h3 = is_I_img_ideal and is_J_img_ideal and (set(sum_IJ_nil) == set(elements))
        
        # Conclusion: The ideals I and J are comaximal in R
        is_I_ideal = is_ideal(elements, add, mul, zero, I)
        is_J_ideal = is_ideal(elements, add, mul, zero, J)
        
        sum_IJ = set()
        for i in I:
            for j in J:
                sum_IJ.add(add(i, j))
                
        q = is_I_ideal and is_J_ideal and (set(sum_IJ) == set(elements))
        neg_q = not q
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Nil(R) is the nilradical of R",
    "H_3: The image of I and the image of J in the quotient ring R/Nil(R) are comaximal",
    "¬Q: The ideals I and J are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3