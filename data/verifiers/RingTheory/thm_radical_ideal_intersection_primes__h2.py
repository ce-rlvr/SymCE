import itertools
import functools
import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects are required for this domain, but standard sympy objects are available.

def get_ring_data(witness):
    """
    Extracts ring data from the witness.
    Expected to have: elements, add, mul, zero, I
    """
    if isinstance(witness, dict):
        elements = witness['elements']
        add = witness['add']
        mul = witness['mul']
        zero = witness['zero']
        I = witness['I']
    else:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        I = witness.I
    return elements, add, mul, zero, I

def is_commutative_ring(elements, add, mul, zero):
    try:
        if zero not in elements: 
            return False
        
        # Check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                
        # Check addition (commutative & associative)
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    
        # Check zero identity
        for a in elements:
            if add(a, zero) != a: return False
            
        # Check additive inverses
        for a in elements:
            has_inv = False
            for b in elements:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check multiplication (commutative & associative)
        for a in elements:
            for b in elements:
                if mul(a, b) != mul(b, a): return False
                for c in elements:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    
        # Check distributive laws
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    
        return True
    except Exception:
        return False

def is_ideal(elements, add, mul, zero, I):
    try:
        if not I: return False
        for val in I:
            if val not in elements: return False
        if zero not in I: return False
        
        # Check additive subgroup
        for a in I:
            for b in I:
                if add(a, b) not in I: return False
                
        for a in I:
            has_inv = False
            for b in I:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check absorption
        for a in I:
            for r in elements:
                if mul(r, a) not in I: return False
                
        return True
    except Exception:
        return False

def is_prime_ideal(elements, add, mul, zero, P):
    if len(P) == len(elements): 
        return False
    for a in elements:
        for b in elements:
            if mul(a, b) in P:
                if a not in P and b not in P:
                    return False
    return True

def get_radical(elements, mul, I):
    rad = set()
    max_pow = len(elements)
    for x in elements:
        curr = x
        in_I = False
        for _ in range(max_pow):
            if curr in I:
                in_I = True
                break
            curr = mul(curr, x)
        if in_I:
            rad.add(x)
    return rad

def conditions(witness):
    try:
        elements, add, mul, zero, I = get_ring_data(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_commutative_ring(elements, add, mul, zero) and is_ideal(elements, add, mul, zero, I)
    except Exception:
        h1 = False
        
    try:
        rad_I = get_radical(elements, mul, I)
        
        def get_ideal_generated_by(gens):
            ideal = set(gens)
            ideal.add(zero)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in ideal:
                    for b in ideal:
                        s = add(a, b)
                        if s not in ideal: new_elements.add(s)
                    for r in elements:
                        p = mul(r, a)
                        if p not in ideal: new_elements.add(p)
                if new_elements:
                    ideal.update(new_elements)
                    changed = True
            return frozenset(ideal)
            
        all_ideals = set()
        principal_ideals = set()
        for x in elements:
            principal_ideals.add(get_ideal_generated_by([x]))
            
        all_ideals.update(principal_ideals)
        
        changed = True
        while changed:
            changed = False
            new_ideals = set()
            for I1 in all_ideals:
                for I2 in all_ideals:
                    sum_ideal = set()
                    for a in I1:
                        for b in I2:
                            sum_ideal.add(add(a, b))
                    fs = frozenset(sum_ideal)
                    if fs not in all_ideals:
                        new_ideals.add(fs)
            if new_ideals:
                all_ideals.update(new_ideals)
                changed = True
                
        prime_ideals_containing_I = []
        for ideal in all_ideals:
            if set(I).issubset(ideal):
                if is_prime_ideal(elements, add, mul, zero, ideal):
                    prime_ideals_containing_I.append(ideal)
                    
        if not prime_ideals_containing_I:
            intersection = set(elements)
        else:
            intersection = set(prime_ideals_containing_I[0])
            for P in prime_ideals_containing_I[1:]:
                intersection = intersection.intersection(P)
                
        neg_q = (rad_I != intersection)
        
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and I is an ideal",
    "¬Q: The radical of I is NOT equal to the intersection of all prime ideals of R that contain I"
]

N_HYP = 1
NEG_Q_INDEX = 1