import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_ring_ops(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], int) and isinstance(witness[1], int):
            n, a = witness
            elements = list(range(n))
            add_func = lambda x, y: (x + y) % n
            mul_func = lambda x, y: (x * y) % n
            zero = 0
            I = list(set((a * x) % n for x in range(n)))
            return elements, add_func, mul_func, zero, I
        if isinstance(witness[0], int) and isinstance(witness[1], list):
            n = witness[0]
            gens = witness[1]
            elements = list(range(n))
            add_func = lambda x, y: (x + y) % n
            mul_func = lambda x, y: (x * y) % n
            zero = 0
            I_set = {0}
            for g in gens:
                I_set.update({(g * x) % n for x in range(n)})
            changed = True
            while changed:
                changed = False
                new_els = set()
                for x in I_set:
                    for y in I_set:
                        s = (x + y) % n
                        if s not in I_set:
                            new_els.add(s)
                if new_els:
                    I_set.update(new_els)
                    changed = True
            return elements, add_func, mul_func, zero, list(I_set)

    if isinstance(witness, dict):
        if 'n' in witness and 'elements' not in witness:
            elements = list(range(witness['n']))
        else:
            elements = list(witness.get('elements', []))
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        if zero is None and 0 in elements:
            zero = 0
        I = list(witness.get('I', []))
    else:
        if hasattr(witness, 'n') and not hasattr(witness, 'elements'):
            elements = list(range(witness.n))
        else:
            elements = list(getattr(witness, 'elements', []))
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        zero = getattr(witness, 'zero', None)
        if zero is None and 0 in elements:
            zero = 0
        I = list(getattr(witness, 'I', []))
        
    if not elements or add is None or mul is None or zero is None:
        raise ValueError("Witness must have elements, add, mul, zero, I")
        
    if len(elements) > 200:
        raise ValueError("Ring too large for verification")
        
    if isinstance(add, dict):
        add_func = lambda a, b: add.get((a, b), add.get((b, a)))
    elif isinstance(add, list):
        def add_func(a, b):
            res = add[elements.index(a)][elements.index(b)]
            if isinstance(res, int) and res < len(elements) and res not in elements:
                return elements[res]
            return res
    else:
        add_func = add

    if isinstance(mul, dict):
        mul_func = lambda a, b: mul.get((a, b), mul.get((b, a)))
    elif isinstance(mul, list):
        def mul_func(a, b):
            res = mul[elements.index(a)][elements.index(b)]
            if isinstance(res, int) and res < len(elements) and res not in elements:
                return elements[res]
            return res
    else:
        mul_func = mul

    return elements, add_func, mul_func, zero, I

def check_commutative_ring(elements, add, mul, zero):
    if zero not in elements: return False
    n = len(elements)
    if n == 0: return False
    
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
        for b in elements:
            s = add(a, b)
            if s not in elements: return False
            if s != add(b, a): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in elements:
        for b in elements:
            p = mul(a, b)
            if p not in elements: return False
            if p != mul(b, a): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    return True

def check_ideal(elements, add, mul, zero, I):
    if not I: return False
    for x in I:
        if x not in elements: return False
        
    for a in I:
        for b in I:
            if add(a, b) not in I: return False
            
    for a in I:
        inv_a = None
        for b in elements:
            if add(a, b) == zero:
                inv_a = b
                break
        if inv_a not in I: return False
        
    for r in elements:
        for x in I:
            if mul(r, x) not in I: return False
            if mul(x, r) not in I: return False
            
    return True

def get_annihilator(elements, mul, zero, I):
    ann = []
    for r in elements:
        is_ann = True
        for x in I:
            if mul(r, x) != zero:
                is_ann = False
                break
        if is_ann:
            ann.append(r)
    return ann

def get_product_ideal(elements, add, mul, zero, A, B):
    prod_ideal = []
    for a in A:
        for b in B:
            p = mul(a, b)
            if p in elements and p not in prod_ideal:
                prod_ideal.append(p)
                
    changed = True
    while changed:
        changed = False
        new_elements = []
        for x in prod_ideal:
            for y in prod_ideal:
                s = add(x, y)
                if s in elements and s not in prod_ideal and s not in new_elements:
                    new_elements.append(s)
        if new_elements:
            prod_ideal.extend(new_elements)
            changed = True
            
    changed = True
    while changed:
        changed = False
        new_elements = []
        for r in elements:
            for x in prod_ideal:
                p1 = mul(r, x)
                if p1 in elements and p1 not in prod_ideal and p1 not in new_elements:
                    new_elements.append(p1)
                p2 = mul(x, r)
                if p2 in elements and p2 not in prod_ideal and p2 not in new_elements:
                    new_elements.append(p2)
        if new_elements:
            prod_ideal.extend(new_elements)
            changed = True
            
    return prod_ideal

def check_conclusion(elements, add, mul, zero, I):
    ann = get_annihilator(elements, mul, zero, I)
    prod = get_product_ideal(elements, add, mul, zero, I, ann)
    
    if len(prod) == 0:
        return True
        
    for x in prod:
        if x != zero:
            return False
    return True

def conditions(witness):
    try:
        elements, add, mul, zero, I = get_ring_ops(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_commutative_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = check_ideal(elements, add, mul, zero, I)
    except Exception:
        h2 = False
        
    try:
        q_holds = check_conclusion(elements, add, mul, zero, I)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: I * Ann(I) != {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2