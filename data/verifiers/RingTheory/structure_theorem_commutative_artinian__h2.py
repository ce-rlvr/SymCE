import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_comm_ring(witness):
    if hasattr(witness, 'is_commutative_ring'):
        if callable(witness.is_commutative_ring):
            return bool(witness.is_commutative_ring())
        return bool(witness.is_commutative_ring)
        
    elements = list(witness.elements)
    
    if hasattr(witness, 'zero'):
        zero = witness.zero
    else:
        zero = None
        for e in elements:
            if all((hasattr(witness, 'add') and witness.add(e, x) == x) or (not hasattr(witness, 'add') and e + x == x) for x in elements):
                zero = e
                break
        if zero is None:
            return False

    if hasattr(witness, 'add'):
        add = witness.add
    else:
        add = lambda a, b: a + b

    if hasattr(witness, 'mul'):
        mul = witness.mul
    else:
        mul = lambda a, b: a * b
        
    if zero not in elements: return False
    
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
        
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            ab_add = add(a, b)
            ab_mul = mul(a, b)
            if ab_add not in elements: return False
            if ab_mul not in elements: return False
            if ab_add != add(b, a): return False
            if ab_mul != mul(b, a): return False
            
            for c in elements:
                if add(a, add(b, c)) != add(ab_add, c): return False
                if mul(a, mul(b, c)) != mul(ab_mul, c): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    return True

def is_artinian_ring(witness):
    if hasattr(witness, 'is_artinian'):
        if callable(witness.is_artinian):
            return bool(witness.is_artinian())
        return bool(witness.is_artinian)
        
    elements = list(witness.elements)
    return len(elements) > 0

def has_ident(witness):
    if hasattr(witness, 'has_identity'):
        if callable(witness.has_identity):
            return bool(witness.has_identity())
        return bool(witness.has_identity)
        
    elements = list(witness.elements)
    if hasattr(witness, 'mul'):
        mul = witness.mul
    else:
        mul = lambda a, b: a * b
        
    for e in elements:
        is_id = True
        for x in elements:
            if mul(e, x) != x or mul(x, e) != x:
                is_id = False
                break
        if is_id:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_comm_ring(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = is_artinian_ring(witness)
    except Exception:
        h2 = False
        
    try:
        # By the Structure Theorem for Commutative Artinian Rings, a commutative Artinian ring 
        # is isomorphic to a finite direct product of Artinian local rings IF AND ONLY IF 
        # it has a multiplicative identity.
        is_art = is_artinian_ring(witness)
        has_id = has_ident(witness)
        is_comm = is_comm_ring(witness)
        
        is_product = is_art and has_id and is_comm
        neg_q = not is_product
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of Artinian local rings"
]

N_HYP = 2
NEG_Q_INDEX = 2