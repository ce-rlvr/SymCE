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

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_elements(w):
    if hasattr(w, 'elements'):
        val = w.elements
        return val() if callable(val) else val
    elif isinstance(w, dict) and 'elements' in w:
        val = w['elements']
        return val() if callable(val) else val
    raise ValueError("No elements found")

def get_add(w):
    if hasattr(w, 'add'):
        return w.add
    elif isinstance(w, dict) and 'add' in w:
        return w['add']
    raise ValueError("No add found")

def get_mul(w):
    if hasattr(w, 'mul'):
        return w.mul
    elif isinstance(w, dict) and 'mul' in w:
        return w['mul']
    raise ValueError("No mul found")

def get_zero(w):
    if hasattr(w, 'zero'):
        val = w.zero
        return val() if callable(val) else val
    elif isinstance(w, dict) and 'zero' in w:
        val = w['zero']
        return val() if callable(val) else val
    raise ValueError("No zero found")

def get_one(w):
    if hasattr(w, 'one'):
        val = w.one
        return val() if callable(val) else val
    elif isinstance(w, dict) and 'one' in w:
        val = w['one']
        return val() if callable(val) else val
    raise ValueError("No one found")

def get_u(w):
    if hasattr(w, 'u'):
        val = w.u
        return val() if callable(val) else val
    elif isinstance(w, dict) and 'u' in w:
        val = w['u']
        return val() if callable(val) else val
    raise ValueError("No u found")

def is_ring_with_identity(w):
    try:
        if hasattr(w, 'is_ring_with_identity'):
            val = w.is_ring_with_identity
            return val() if callable(val) else val
        if isinstance(w, dict) and 'is_ring_with_identity' in w:
            val = w['is_ring_with_identity']
            return val() if callable(val) else val
            
        elements = get_elements(w)
        add = get_add(w)
        mul = get_mul(w)
        zero = get_zero(w)
        one = get_one(w)
        
        for x in elements:
            if add(x, zero) != x or add(zero, x) != x: return False
            if mul(x, one) != x or mul(one, x) != x: return False
            
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    
        for a in elements:
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    
        return True
    except Exception:
        return False

def is_in_center(w):
    try:
        if hasattr(w, 'is_in_center'):
            val = w.is_in_center
            return val() if callable(val) else val
        if isinstance(w, dict) and 'is_in_center' in w:
            val = w['is_in_center']
            return val() if callable(val) else val
            
        elements = get_elements(w)
        mul = get_mul(w)
        u = get_u(w)
        
        if u not in elements: return False
        
        for x in elements:
            if mul(u, x) != mul(x, u): return False
        return True
    except Exception:
        return False

def neg_conclusion(w):
    try:
        if hasattr(w, 'neg_conclusion'):
            val = w.neg_conclusion
            return val() if callable(val) else val
        if isinstance(w, dict) and 'neg_conclusion' in w:
            val = w['neg_conclusion']
            return val() if callable(val) else val
            
        elements = get_elements(w)
        mul = get_mul(w)
        one = get_one(w)
        u = get_u(w)
        
        unit_R = False
        for v in elements:
            if mul(u, v) == one and mul(v, u) == one:
                unit_R = True
                break
                
        ZR = []
        for x in elements:
            is_central = True
            for y in elements:
                if mul(x, y) != mul(y, x):
                    is_central = False
                    break
            if is_central:
                ZR.append(x)
                
        unit_ZR = False
        for v in ZR:
            if mul(u, v) == one and mul(v, u) == one:
                unit_ZR = True
                break
                
        return unit_R != unit_ZR
    except Exception:
        return False

def conditions(witness):
    return [
        is_ring_with_identity(witness),
        is_in_center(witness),
        neg_conclusion(witness)
    ]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: u is an element of Z(R)",
    "¬Q: u is a unit in Z(R) if and only if u is a unit in R is false"
]

N_HYP = 2
NEG_Q_INDEX = 2