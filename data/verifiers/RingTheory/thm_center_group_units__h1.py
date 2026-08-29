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

# Top-level setup: named object bindings
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

class FiniteRing:
    """
    A generic finite ring protocol class.
    Witnesses should implement this protocol or be an instance of this class.
    """
    def __init__(self, elements, zero, one, add_func, mul_func, eq_func=lambda x, y: x == y):
        self.elements = elements
        self.zero = zero
        self.one = one
        self._add = add_func
        self._mul = mul_func
        self._eq = eq_func
        
    def add(self, x, y): return self._add(x, y)
    def mul(self, x, y): return self._mul(x, y)
    def eq(self, x, y): return self._eq(x, y)

class UpperTriangularMatrixRingMod4:
    """
    The ring of 2x2 upper triangular matrices over Z/4Z.
    This is a known counterexample where Z(U(R)) != U(Z(R)).
    Elements are represented as tuples (a, b, c) corresponding to:
    [a, b]
    [0, c]
    """
    def __init__(self):
        self.elements = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]
        self.zero = (0, 0, 0)
        self.one = (1, 0, 1)
        
    def add(self, x, y):
        return ((x[0] + y[0]) % 4, (x[1] + y[1]) % 4, (x[2] + y[2]) % 4)
        
    def mul(self, x, y):
        return ((x[0] * y[0]) % 4, (x[0] * y[1] + x[1] * y[2]) % 4, (x[2] * y[2]) % 4)
        
    def eq(self, x, y):
        return x == y

# Provide the counterexample in the namespace
R_counterexample = UpperTriangularMatrixRingMod4()
Z4_UpperTriangular = R_counterexample

def is_ring(R):
    try:
        elements = []
        for i, e in enumerate(R.elements):
            if i > 500:  # Prevent infinite loops for infinite rings
                return False
            elements.append(e)
            
        zero = R.zero
        one = R.one
        
        if not any(R.eq(zero, e) for e in elements): return False
        if not any(R.eq(one, e) for e in elements): return False
        
        for a in elements:
            if not R.eq(R.add(a, zero), a): return False
            if not R.eq(R.add(zero, a), a): return False
            if not R.eq(R.mul(a, one), a): return False
            if not R.eq(R.mul(one, a), a): return False
            
            has_inv = False
            for b in elements:
                if R.eq(R.add(a, b), zero) and R.eq(R.add(b, a), zero):
                    has_inv = True
                    break
            if not has_inv: return False
            
        for a in elements:
            for b in elements:
                sum_ab = R.add(a, b)
                prod_ab = R.mul(a, b)
                if not any(R.eq(sum_ab, e) for e in elements): return False
                if not any(R.eq(prod_ab, e) for e in elements): return False
                
        subset = elements[:20] if len(elements) > 20 else elements
        for a, b, c in itertools.product(subset, repeat=3):
            if not R.eq(R.add(R.add(a, b), c), R.add(a, R.add(b, c))): return False
            if not R.eq(R.add(a, b), R.add(b, a)): return False
            if not R.eq(R.mul(R.mul(a, b), c), R.mul(a, R.mul(b, c))): return False
            if not R.eq(R.mul(a, R.add(b, c)), R.add(R.mul(a, b), R.mul(a, c))): return False
            if not R.eq(R.mul(R.add(a, b), c), R.add(R.mul(a, c), R.mul(b, c))): return False
            
        return True
    except Exception:
        return False

def get_U(R):
    elements = list(R.elements)
    units = []
    for a in elements:
        has_left = False
        has_right = False
        for b in elements:
            if R.eq(R.mul(a, b), R.one):
                has_right = True
            if R.eq(R.mul(b, a), R.one):
                has_left = True
        if has_left and has_right:
            units.append(a)
    return units

def get_Z(R):
    elements = list(R.elements)
    center = []
    for a in elements:
        is_center = True
        for x in elements:
            if not R.eq(R.mul(a, x), R.mul(x, a)):
                is_center = False
                break
        if is_center:
            center.append(a)
    return center

def get_Z_U(R, U):
    z_u = []
    for u in U:
        is_center = True
        for x in U:
            if not R.eq(R.mul(u, x), R.mul(x, u)):
                is_center = False
                break
        if is_center:
            z_u.append(u)
    return z_u

def get_U_Z(R, Z):
    u_z = []
    for a in Z:
        has_inv = False
        for b in Z:
            if R.eq(R.mul(a, b), R.one) and R.eq(R.mul(b, a), R.one):
                has_inv = True
                break
        if has_inv:
            u_z.append(a)
    return u_z

def conditions(witness):
    try:
        ring_ok = is_ring(witness)
    except Exception:
        ring_ok = False

    h1 = ring_ok
    h2 = ring_ok

    neg_q = False
    if ring_ok:
        try:
            U = get_U(witness)
            Z = get_Z(witness)
            Z_U = get_Z_U(witness, U)
            U_Z = get_U_Z(witness, Z)
            
            def is_subset(A, B):
                for a in A:
                    found = False
                    for b in B:
                        if witness.eq(a, b):
                            found = True
                            break
                    if not found:
                        return False
                return True
                
            same_sets = is_subset(Z_U, U_Z) and is_subset(U_Z, Z_U)
            neg_q = not same_sets
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let U(R) denote the group of units of R",
    "H_2: Let Z(R) denote the center of the ring R",
    "¬Q: Z(U(R)) != U(Z(R))"
]

N_HYP = 2
NEG_Q_INDEX = 2