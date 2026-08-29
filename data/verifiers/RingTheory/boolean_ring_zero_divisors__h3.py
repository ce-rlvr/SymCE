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

class BooleanRingZ2xZ2:
    def __init__(self):
        self.elements = [(0,0), (0,1), (1,0), (1,1)]
        self.zero = (0,0)
        self.one = (1,1)
    def add(self, a, b):
        return ((a[0]+b[0])%2, (a[1]+b[1])%2)
    def mul(self, a, b):
        return ((a[0]*b[0])%2, (a[1]*b[1])%2)
    def __str__(self):
        return "Z2xZ2"

class BooleanRingZ2xZ2xZ2:
    def __init__(self):
        self.elements = [(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)]
        self.zero = (0,0,0)
        self.one = (1,1,1)
    def add(self, a, b):
        return ((a[0]+b[0])%2, (a[1]+b[1])%2, (a[2]+b[2])%2)
    def mul(self, a, b):
        return ((a[0]*b[0])%2, (a[1]*b[1])%2, (a[2]*b[2])%2)
    def __str__(self):
        return "Z2xZ2xZ2"

# Top-level setup bindings
Z2xZ2 = BooleanRingZ2xZ2()
Z2xZ2xZ2 = BooleanRingZ2xZ2xZ2()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        else:
            R = witness.R
            x = witness.x
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring with a multiplicative identity 1
    h1_ok = False
    try:
        elements = list(R.elements)
        if len(elements) > 256:
            h1_ok = False
        else:
            zero = R.zero
            one = R.one
            
            is_ring = True
            if zero not in elements or one not in elements:
                is_ring = False
            if zero == one and len(elements) > 1:
                is_ring = False
                
            if is_ring:
                for a in elements:
                    if R.add(a, zero) != a: is_ring = False; break
                    if R.add(zero, a) != a: is_ring = False; break
                    if R.mul(a, one) != a: is_ring = False; break
                    if R.mul(one, a) != a: is_ring = False; break
                    if R.mul(a, a) != a: is_ring = False; break
                    if R.add(a, a) != zero: is_ring = False; break
                    for b in elements:
                        if R.add(a, b) != R.add(b, a): is_ring = False; break
                        if R.mul(a, b) != R.mul(b, a): is_ring = False; break
                        for c in elements:
                            if R.add(a, R.add(b, c)) != R.add(R.add(a, b), c): is_ring = False; break
                            if R.mul(a, R.mul(b, c)) != R.mul(R.mul(a, b), c): is_ring = False; break
                            if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): is_ring = False; break
                    if not is_ring: break
            h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H_2: The cardinality of R is strictly greater than 2
    h2_ok = False
    try:
        h2_ok = len(list(R.elements)) > 2
    except Exception:
        h2_ok = False

    # ¬Q: x is not a zero divisor in R
    neg_q_ok = False
    try:
        if x not in list(R.elements):
            neg_q_ok = False
        else:
            is_zd = False
            if x != R.zero:
                for y in list(R.elements):
                    if y != R.zero and R.mul(x, y) == R.zero:
                        is_zd = True
                        break
            neg_q_ok = not is_zd
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity 1",
    "H_2: The cardinality of R is strictly greater than 2",
    "¬Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2