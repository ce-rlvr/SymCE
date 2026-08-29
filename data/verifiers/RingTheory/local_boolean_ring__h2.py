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

class Ring:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

Z2 = Ring([0, 1], lambda x, y: (x + y) % 2, lambda x, y: (x * y) % 2, 0)
Z3 = Ring([0, 1, 2], lambda x, y: (x + y) % 3, lambda x, y: (x * y) % 3, 0)
Z4 = Ring([0, 1, 2, 3], lambda x, y: (x + y) % 4, lambda x, y: (x * y) % 4, 0)
Z6 = Ring([0, 1, 2, 3, 4, 5], lambda x, y: (x + y) % 6, lambda x, y: (x * y) % 6, 0)

Z2xZ2 = Ring(
    [(0,0), (0,1), (1,0), (1,1)],
    lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2),
    lambda x, y: ((x[0]*y[0])%2, (x[1]*y[1])%2),
    (0,0)
)

Z2xZ2xZ2 = Ring(
    list(itertools.product([0,1], repeat=3)),
    lambda x, y: tuple((a+b)%2 for a, b in zip(x, y)),
    lambda x, y: tuple((a*b)%2 for a, b in zip(x, y)),
    (0,0,0)
)

def is_boolean_ring(R):
    try:
        elements = R.elements
        zero = R.zero
        
        if not elements:
            return False
            
        if zero not in elements:
            return False

        # Check closure, associativity, commutativity of addition, and distributivity
        for a in elements:
            for b in elements:
                sum_ab = R.add(a, b)
                prod_ab = R.mul(a, b)
                if sum_ab not in elements: return False
                if prod_ab not in elements: return False
                if sum_ab != R.add(b, a): return False
                
                for c in elements:
                    if R.add(sum_ab, c) != R.add(a, R.add(b, c)): return False
                    if R.mul(prod_ab, c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(prod_ab, R.mul(a, c)): return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
        
        # Check additive identity
        for a in elements:
            if R.add(a, zero) != a: return False
            
        # Check additive inverse
        for a in elements:
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False

        # Check Boolean property: x^2 = x
        for a in elements:
            if R.mul(a, a) != a: return False

        # Check multiplicative identity
        has_one = False
        for e in elements:
            is_one = True
            for a in elements:
                if R.mul(e, a) != a or R.mul(a, e) != a:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False

        return True
    except Exception:
        return False

def is_iso_z2(R):
    try:
        if len(R.elements) != 2:
            return False
        zero = R.zero
        others = [e for e in R.elements if e != zero]
        if len(others) != 1:
            return False
        x = others[0]
        if R.add(x, x) != zero:
            return False
        if R.mul(x, x) != x:
            return False
        if R.mul(x, zero) != zero or R.mul(zero, x) != zero:
            return False
        if R.add(x, zero) != x or R.add(zero, x) != x:
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_boolean_ring(witness)
    except Exception:
        h1 = False

    try:
        if not hasattr(witness, 'elements'):
            neg_q = False
        else:
            neg_q = not is_iso_z2(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1