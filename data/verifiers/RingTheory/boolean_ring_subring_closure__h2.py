import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_boolean_ring(R, add, mul):
    if not R: return False
    try:
        R = list(R)
    except TypeError:
        return False
        
    # check closure
    for a in R:
        for b in R:
            try:
                if add(a, b) not in R: return False
                if mul(a, b) not in R: return False
            except Exception:
                return False
                
    # check abelian group for addition
    zero = None
    for z_elem in R:
        try:
            if all(add(a, z_elem) == a and add(z_elem, a) == a for a in R):
                zero = z_elem
                break
        except Exception:
            pass
    if zero is None: return False
    
    # inverses
    for a in R:
        try:
            if not any(add(a, b) == zero and add(b, a) == zero for b in R):
                return False
        except Exception:
            return False
            
    # associativity and distributivity
    for a in R:
        for b in R:
            for c in R:
                try:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                except Exception:
                    return False
                
    # commutativity of addition
    for a in R:
        for b in R:
            try:
                if add(a, b) != add(b, a): return False
            except Exception:
                return False
            
    # boolean property
    for a in R:
        try:
            if mul(a, a) != a: return False
        except Exception:
            return False
        
    return True

def is_subring(S, R, add, mul):
    if not S: return False
    try:
        S = list(S)
        R = list(R)
    except TypeError:
        return False
        
    if not all(elem in R for elem in S): return False
    
    zero_R = None
    for z_elem in R:
        try:
            if all(add(a, z_elem) == a and add(z_elem, a) == a for a in R):
                zero_R = z_elem
                break
        except Exception:
            pass
            
    if zero_R not in S: return False
    
    for a in S:
        for b in S:
            try:
                if add(a, b) not in S: return False
                if mul(a, b) not in S: return False
            except Exception:
                return False
                
    for a in S:
        try:
            if not any(add(a, b) == zero_R and add(b, a) == zero_R for b in S):
                return False
        except Exception:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', [])
            S = witness.get('S', [])
            add = witness.get('add', None)
            mul = witness.get('mul', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                R, S = witness
                add, mul = None, None
            elif len(witness) == 4:
                R, S, add, mul = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        if add is None:
            def add(a, b):
                if isinstance(a, (set, frozenset)): return a ^ b
                return a ^ b
        if mul is None:
            def mul(a, b):
                if isinstance(a, (set, frozenset)): return a & b
                return a & b
                
        h1 = is_boolean_ring(R, add, mul)
        
        # The conclusion is "The subring S is a Boolean ring."
        # This fails if S is not a subring, or if S is not a Boolean ring.
        q = is_subring(S, R, add, mul) and is_boolean_ring(S, add, mul)
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The subring S is not a Boolean ring (or S is not a subring)"
]
N_HYP = 1
NEG_Q_INDEX = 1