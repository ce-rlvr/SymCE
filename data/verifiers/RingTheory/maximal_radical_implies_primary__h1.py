import itertools
import math
import functools
import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

def get_elements(witness):
    if hasattr(witness, 'elements'): return witness.elements
    if hasattr(witness, 'ring_elements'): return witness.ring_elements
    return list(witness.R)

def get_I(witness):
    if hasattr(witness, 'I'): return witness.I
    if hasattr(witness, 'ideal'): return witness.ideal
    return list(witness.I_elements)

def get_add(witness):
    if hasattr(witness, 'add'): return witness.add
    return lambda a, b: a + b

def get_mul(witness):
    if hasattr(witness, 'mul'): return witness.mul
    return lambda a, b: a * b

def get_zero(witness):
    if hasattr(witness, 'zero'): return witness.zero
    return 0

def check_h1(witness):
    if hasattr(witness, 'is_proper_ideal'):
        return bool(witness.is_proper_ideal())
    
    elements = get_elements(witness)
    I = get_I(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    zero = get_zero(witness)
    
    if len(I) == len(elements): 
        return False
    
    I_set = set(I)
    if zero not in I_set: 
        return False
    
    for a in I:
        for b in I:
            if add(a, b) not in I_set: 
                return False
            
    for a in I:
        for r in elements:
            if mul(a, r) not in I_set: 
                return False
            if mul(r, a) not in I_set: 
                return False
            
    return True

def check_h2(witness):
    if hasattr(witness, 'is_sqrt_maximal'):
        return bool(witness.is_sqrt_maximal())
    
    elements = get_elements(witness)
    I = get_I(witness)
    add = get_add(witness)
    mul = get_mul(witness)
    zero = get_zero(witness)
    
    I_set = set(I)
    sqrt_I = []
    for elem in elements:
        curr = elem
        found = False
        for _ in range(len(elements) + 1):
            if curr in I_set:
                found = True
                break
            curr = mul(curr, elem)
        if found:
            sqrt_I.append(elem)
            
    sqrt_I_set = set(sqrt_I)
    
    if zero not in sqrt_I_set: 
        return False
        
    for a in sqrt_I:
        for b in sqrt_I:
            if add(a, b) not in sqrt_I_set: 
                return False
                
    for a in sqrt_I:
        for r in elements:
            if mul(a, r) not in sqrt_I_set: 
                return False
            if mul(r, a) not in sqrt_I_set: 
                return False
            
    if len(sqrt_I) == len(elements): 
        return False
    
    for elem in elements:
        if elem in sqrt_I_set: 
            continue
        
        gen = set(sqrt_I)
        gen.add(elem)
        
        added = True
        while added:
            added = False
            new_elements = set()
            for g in gen:
                for r in elements:
                    m1 = mul(g, r)
                    if m1 not in gen and m1 not in new_elements:
                        new_elements.add(m1)
                    m2 = mul(r, g)
                    if m2 not in gen and m2 not in new_elements:
                        new_elements.add(m2)
            if new_elements:
                gen.update(new_elements)
                added = True
                
        added = True
        while added:
            added = False
            new_elements = set()
            for a in gen:
                for b in gen:
                    s = add(a, b)
                    if s not in gen and s not in new_elements:
                        new_elements.add(s)
            if new_elements:
                gen.update(new_elements)
                added = True
                
        if len(gen) != len(elements):
            return False
            
    return True

def check_neg_q(witness):
    if hasattr(witness, 'is_primary'):
        return not bool(witness.is_primary())
    
    elements = get_elements(witness)
    I = get_I(witness)
    
    if len(I) == len(elements):
        return True
        
    add = get_add(witness)
    mul = get_mul(witness)
    
    I_set = set(I)
    
    sqrt_I = []
    for elem in elements:
        curr = elem
        found = False
        for _ in range(len(elements) + 1):
            if curr in I_set:
                found = True
                break
            curr = mul(curr, elem)
        if found:
            sqrt_I.append(elem)
    sqrt_I_set = set(sqrt_I)
    
    is_primary = True
    for a in elements:
        for b in elements:
            if mul(a, b) in I_set:
                if a not in I_set and b not in sqrt_I_set:
                    is_primary = False
                    break
        if not is_primary:
            break
            
    return not is_primary

def conditions(witness) -> list[bool]:
    try:
        h1 = check_h1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_h2(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: The radical \\sqrt{I} is a maximal ideal of R",
    "¬Q: I is not a primary ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2