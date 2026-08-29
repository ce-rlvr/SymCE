import itertools
import functools
import math
from sympy import Matrix, eye, zeros

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one, eq=None):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one
        self.eq = eq if eq is not None else lambda x, y: x == y

    def is_local(self):
        if self.eq(self.zero, self.one):
            return False
        units = []
        for a in self.elements:
            is_unit = False
            for b in self.elements:
                if self.eq(self.mul(a, b), self.one) and self.eq(self.mul(b, a), self.one):
                    is_unit = True
                    break
            if is_unit:
                units.append(a)
                
        non_units = []
        for a in self.elements:
            if not any(self.eq(a, u) for u in units):
                non_units.append(a)
                
        for a in non_units:
            for b in non_units:
                s = self.add(a, b)
                if not any(self.eq(s, nu) for nu in non_units):
                    return False
        return True

    def center(self):
        c_elements = []
        for a in self.elements:
            if all(self.eq(self.mul(a, x), self.mul(x, a)) for x in self.elements):
                c_elements.append(a)
        return FiniteRing(c_elements, self.add, self.mul, self.zero, self.one, self.eq)

def MatrixRingMod(n, d):
    elements = []
    for entries in itertools.product(range(n), repeat=d*d):
        elements.append(Matrix(d, d, entries))
    
    def add(A, B):
        return (A + B).applyfunc(lambda x: x % n)
        
    def mul(A, B):
        return (A * B).applyfunc(lambda x: x % n)
        
    zero = zeros(d, d)
    one = eye(d)
    
    def eq(A, B):
        return A == B
        
    return FiniteRing(elements, add, mul, zero, one, eq)

def Subring(ring, generators):
    elements = []
    queue = list(generators)
    if not any(ring.eq(ring.one, g) for g in queue):
        queue.append(ring.one)
    if not any(ring.eq(ring.zero, g) for g in queue):
        queue.append(ring.zero)
        
    for g in queue:
        if not any(ring.eq(g, e) for e in elements):
            elements.append(g)
            
    added = True
    while added:
        added = False
        n_elems = len(elements)
        for i in range(n_elems):
            for j in range(n_elems):
                s = ring.add(elements[i], elements[j])
                if not any(ring.eq(s, e) for e in elements):
                    elements.append(s)
                    added = True
                p = ring.mul(elements[i], elements[j])
                if not any(ring.eq(p, e) for e in elements):
                    elements.append(p)
                    added = True
    return FiniteRing(elements, ring.add, ring.mul, ring.zero, ring.one, ring.eq)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, Z_R = witness
        else:
            R = witness
            Z_R = R.center()
    except Exception:
        return [False, False, False]

    try:
        h1 = R.is_local()
    except Exception:
        h1 = False

    try:
        def is_subset(list1, list2, eq):
            for e1 in list1:
                if not any(eq(e1, e2) for e2 in list2):
                    return False
            return True
        
        actual_center = R.center()
        eq_func = getattr(R, 'eq', lambda x, y: x == y)
        h2 = is_subset(Z_R.elements, actual_center.elements, eq_func) and \
             is_subset(actual_center.elements, Z_R.elements, eq_func)
    except Exception:
        h2 = False

    try:
        neg_q = not Z_R.is_local()
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "H_2: Z(R) is the center of the ring R",
    "¬Q: Z(R) is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2