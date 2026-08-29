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

# Top-level setup: Standard Boolean rings
class Z2Ring:
    elements = [0, 1]
    zero = 0
    one = 1
    @staticmethod
    def add(a, b): return (a + b) % 2
    @staticmethod
    def mul(a, b): return (a * b) % 2

class Z2xZ2Ring:
    elements = [(0,0), (0,1), (1,0), (1,1)]
    zero = (0,0)
    one = (1,1)
    @staticmethod
    def add(a, b): return ((a[0]+b[0])%2, (a[1]+b[1])%2)
    @staticmethod
    def mul(a, b): return ((a[0]*b[0])%2, (a[1]*b[1])%2)

Z2 = Z2Ring
Z2xZ2 = Z2xZ2Ring

def contains(lst, item):
    for x in lst:
        try:
            if bool(x == item): return True
        except Exception:
            pass
    return False

def is_boolean_ring_with_identity(R):
    if R is None: return False
    if R == sympy.GF(2): return True
    try:
        elements = R.elements
        zero = R.zero
        one = R.one
        add = R.add
        mul = R.mul
        
        if len(elements) > 64: return False
        if not contains(elements, zero): return False
        if not contains(elements, one): return False
        
        for a in elements:
            if bool(add(a, zero) != a): return False
            if bool(add(zero, a) != a): return False
            if bool(mul(a, one) != a): return False
            if bool(mul(one, a) != a): return False
            if bool(mul(a, a) != a): return False  # Boolean ring property
            
            inv_exists = False
            for b in elements:
                if bool(add(a, b) == zero) and bool(add(b, a) == zero):
                    inv_exists = True
                    break
            if not inv_exists: return False
            
            for b in elements:
                if not contains(elements, add(a, b)): return False
                if not contains(elements, mul(a, b)): return False
                if bool(add(a, b) != add(b, a)): return False
                
                for c in elements:
                    if bool(add(add(a, b), c) != add(a, add(b, c))): return False
                    if bool(mul(mul(a, b), c) != mul(a, mul(b, c))): return False
                    if bool(mul(a, add(b, c)) != add(mul(a, b), mul(a, c))): return False
                    if bool(mul(add(a, b), c) != add(mul(a, c), mul(b, c))): return False
        return True
    except Exception:
        return False

def is_in_ring(u, R):
    if R == sympy.GF(2):
        try:
            if bool(u == 0) or bool(u == 1): return True
            return u in R
        except Exception:
            return False
    try:
        for el in R.elements:
            if bool(u == el):
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    R = None
    u = None
    
    # Unpack witness if it's a tuple (R, u)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, u = witness
    else:
        u = witness

    # If R is not explicitly provided, try to infer it from u
    if R is None:
        try:
            if bool(u == 0) or bool(u == 1) or bool(u == sympy.S.Zero) or bool(u == sympy.S.One):
                R = Z2Ring
            elif isinstance(u, tuple) and len(u) == 2 and all(bool(x == 0) or bool(x == 1) for x in u):
                R = Z2xZ2Ring
            else:
                R = Z2Ring
        except Exception:
            R = Z2Ring

    # H_1: R is a Boolean ring with identity (and u is an element of R)
    try:
        h1 = bool(is_boolean_ring_with_identity(R) and is_in_ring(u, R))
    except Exception:
        h1 = False

    # ¬Q: u is not equal to the multiplicative identity 1
    try:
        if R == sympy.GF(2):
            neg_q = bool(u != 1)
        else:
            neg_q = bool(u != R.one)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with identity",
    "¬Q: u is not equal to the multiplicative identity 1"
]

N_HYP = 1
NEG_Q_INDEX = 1