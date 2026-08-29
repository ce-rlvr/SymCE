import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero, one):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero
        self.one = one

def conditions(witness) -> list[bool]:
    try:
        ring, I, J, n = witness
    except Exception:
        return [False, False, False]
        
    def check_h1():
        elements = ring.elements
        zero = ring.zero
        one = ring.one
        eq = getattr(ring, 'eq', lambda a, b: a == b)
        
        def contains(lst, item):
            return any(eq(x, item) for x in lst)
            
        # Check if R is a ring
        for a in elements:
            for b in elements:
                if not contains(elements, ring.add(a, b)): return False
                if not contains(elements, ring.mul(a, b)): return False
                
        for a in elements:
            if not eq(ring.add(a, zero), a): return False
            if not eq(ring.add(zero, a), a): return False
            if not eq(ring.mul(a, one), a): return False
            if not eq(ring.mul(one, a), a): return False
            
        for a in elements:
            has_inv = False
            for b in elements:
                if eq(ring.add(a, b), zero) and eq(ring.add(b, a), zero):
                    has_inv = True
                    break
            if not has_inv: return False
            
        test_elements = elements if len(elements) <= 20 else elements[:20]
        for a in test_elements:
            for b in test_elements:
                if not eq(ring.add(a, b), ring.add(b, a)): return False
                for c in test_elements:
                    if not eq(ring.add(ring.add(a, b), c), ring.add(a, ring.add(b, c))): return False
                    if not eq(ring.mul(ring.mul(a, b), c), ring.mul(a, ring.mul(b, c))): return False
                    if not eq(ring.mul(a, ring.add(b, c)), ring.add(ring.mul(a, b), ring.mul(a, c))): return False
                    if not eq(ring.mul(ring.add(a, b), c), ring.add(ring.mul(a, c), ring.mul(b, c))): return False

        # Check if I is an ideal
        if not I: return False
        for a in I:
            if not contains(elements, a): return False
            for b in I:
                if not contains(I, ring.add(a, b)): return False
        for s in I:
            for r in elements:
                if not contains(I, ring.mul(r, s)): return False
                if not contains(I, ring.mul(s, r)): return False
                
        # Check if J is an ideal
        if not J: return False
        for a in J:
            if not contains(elements, a): return False
            for b in J:
                if not contains(J, ring.add(a, b)): return False
        for s in J:
            for r in elements:
                if not contains(J, ring.mul(r, s)): return False
                if not contains(J, ring.mul(s, r)): return False
                
        # Check if comaximal
        comaximal = False
        for i in I:
            for j in J:
                if eq(ring.add(i, j), one):
                    comaximal = True
                    break
            if comaximal:
                break
        if not comaximal:
            return False
            
        return True

    try:
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(n, int) and n >= 0
    except Exception:
        h2_ok = False

    def check_neg_q():
        eq = getattr(ring, 'eq', lambda a, b: a == b)
        def contains(lst, item):
            return any(eq(x, item) for x in lst)
            
        if n == 0:
            return False
        elif n == 1:
            I_cap_J = [x for x in I if contains(J, x)]
            
            products = []
            for i in I:
                for j in J:
                    p = ring.mul(i, j)
                    if not contains(products, p):
                        products.append(p)
            
            IJ = list(products)
            idx = 0
            while idx < len(IJ):
                curr = IJ[idx]
                for p in products:
                    nxt = ring.add(curr, p)
                    if not contains(IJ, nxt):
                        IJ.append(nxt)
                idx += 1
                
            for x in I_cap_J:
                if not contains(IJ, x):
                    return True
            return False
        else:
            raise NotImplementedError("Tor_n for n > 1 not implemented")

    try:
        neg_q_ok = check_neg_q()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I and J are comaximal ideals of R",
    "H_2: n is a non-negative integer",
    "¬Q: The torsion group Tor_n^R(R/I, R/J) is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2