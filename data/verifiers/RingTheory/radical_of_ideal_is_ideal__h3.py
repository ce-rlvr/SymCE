import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, item):
    for e in lst:
        if e == item:
            return True
    return False

def get_ring_components(witness):
    if isinstance(witness, dict):
        return list(witness['elements']), witness['add'], witness['mul'], witness['zero'], list(witness['I'])
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            return list(witness[0]), witness[1], witness[2], witness[3], list(witness[4])
        elif len(witness) == 2:
            R, I = witness
            if hasattr(R, 'elements'):
                return list(R.elements), R.add, R.mul, R.zero, list(I)
            elif isinstance(R, dict):
                return list(R['elements']), R['add'], R['mul'], R['zero'], list(I)
    return list(witness.elements), witness.add, witness.mul, witness.zero, list(witness.I)

def check_H1(elements, add, mul, zero):
    n = len(elements)
    if n == 0: return False
    
    if not contains(elements, zero):
        return False

    for x in elements:
        if add(x, zero) != x or add(zero, x) != x:
            return False
            
    for x in elements:
        has_inv = False
        for y in elements:
            if add(x, y) == zero and add(y, x) == zero:
                has_inv = True
                break
        if not has_inv:
            return False
            
    for x in elements:
        for y in elements:
            s1 = add(x, y)
            s2 = add(y, x)
            if not contains(elements, s1): return False
            if s1 != s2: return False
            
    for x in elements:
        for y in elements:
            for z in elements:
                if add(add(x, y), z) != add(x, add(y, z)):
                    return False
                    
    for x in elements:
        for y in elements:
            p1 = mul(x, y)
            p2 = mul(y, x)
            if not contains(elements, p1): return False
            if p1 != p2: return False
            
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(mul(x, y), z) != mul(x, mul(y, z)):
                    return False
                    
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                    return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)):
                    return False
                    
    return True

def check_H2(elements, add, mul, zero, I):
    if not I: return False
    for x in I:
        if not contains(elements, x): return False
        
    if not contains(I, zero): return False
    
    for x in I:
        for y in I:
            if not contains(I, add(x, y)): return False
            
    for x in I:
        has_inv = False
        for y in I:
            if add(x, y) == zero and add(y, x) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for x in I:
        for r in elements:
            if not contains(I, mul(r, x)): return False
            if not contains(I, mul(x, r)): return False
            
    return True

def check_neg_Q(elements, add, mul, zero, I):
    radical = []
    n = len(elements)
    for x in elements:
        curr = x
        in_rad = False
        for k in range(1, n + 2):
            if contains(I, curr):
                in_rad = True
                break
            curr = mul(curr, x)
        if in_rad:
            radical.append(x)
            
    if not radical: return True
    if not contains(radical, zero): return True
    
    for x in radical:
        for y in radical:
            if not contains(radical, add(x, y)): return True
            
    for x in radical:
        has_inv = False
        for y in radical:
            if add(x, y) == zero and add(y, x) == zero:
                has_inv = True
                break
        if not has_inv: return True
        
    for x in radical:
        for r in elements:
            if not contains(radical, mul(r, x)): return True
            if not contains(radical, mul(x, r)): return True
            
    return False

def conditions(witness):
    try:
        elements, add, mul, zero, I = get_ring_components(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = check_H1(elements, add, mul, zero)
    except Exception:
        h1 = False

    try:
        h2 = check_H2(elements, add, mul, zero, I)
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_Q(elements, add, mul, zero, I)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: \\sqrt{I} is not an ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2