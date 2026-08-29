import sympy
from sympy import S, Range, ImageSet, FiniteSet, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
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

Z = S.Integers
Q = S.Rationals
R = S.Reals
N = S.Naturals

def get_elements_and_membership(witness):
    if isinstance(witness, (int, sympy.Integer)):
        n = int(witness)
        elements = [n * i for i in range(-20, 21)]
        def in_ring(val):
            if n == 0: return val == 0
            if not isinstance(val, (int, sympy.Integer)): return False
            return val % n == 0
        return elements, in_ring

    if witness == sympy.S.Integers:
        elements = list(range(-20, 21))
        def in_ring(val):
            return getattr(sympy.sympify(val), 'is_integer', False)
        return elements, in_ring

    if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
        elements = [sympy.Rational(1, 2), 1, 2]
        def in_ring(val):
            return True
        return elements, in_ring

    if isinstance(witness, sympy.ImageSet):
        try:
            inter = witness.intersect(sympy.Range(-50, 51))
            elements = list(inter)
        except Exception:
            elements = []
        def in_ring(val):
            try:
                return sympy.sympify(val) in witness
            except Exception:
                return False
        if elements:
            return elements, in_ring

    if hasattr(witness, '__iter__'):
        try:
            elements = list(witness)
            def in_ring(val):
                return val in elements
            return elements, in_ring
        except Exception:
            pass
            
    if hasattr(witness, 'intersect'):
        try:
            inter = witness.intersect(sympy.Range(-50, 51))
            elements = list(inter)
            def in_ring(val):
                try:
                    return sympy.sympify(val) in witness
                except Exception:
                    return False
            return elements, in_ring
        except Exception:
            pass

    return [], lambda val: False

def is_euclidean(witness):
    elements, in_ring = get_elements_and_membership(witness)
    if not elements:
        return False
        
    try:
        if not in_ring(1):
            return False
    except Exception:
        return False

    for a in elements:
        if not (isinstance(a, int) or getattr(a, 'is_integer', False)):
            return False

    for a in elements:
        for b in elements:
            try:
                if not in_ring(a + b): return False
                if not in_ring(a * b): return False
                if not in_ring(-a): return False
            except Exception:
                return False

    for a in elements:
        for b in elements:
            if b == 0: continue
            found = False
            try:
                b_int = int(b)
            except Exception:
                return False
            for r in range(-abs(b_int) + 1, abs(b_int)):
                try:
                    if in_ring(r):
                        if (a - r) % b_int == 0:
                            q = (a - r) // b_int
                            if in_ring(q):
                                found = True
                                break
                except Exception:
                    pass
            if not found:
                return False
                
    return True

def conditions(witness):
    # H_1: Let d: Z \ {0} -> N be defined by d(n) = |n|
    # This is a definitional hypothesis, so it holds by setup.
    h1_ok = True
    
    try:
        q_ok = is_euclidean(witness)
    except Exception:
        q_ok = False
        
    neg_q_ok = not q_ok
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: d is defined as d(n) = |n| on Z \\ {0}",
    "¬Q: R is not a Euclidean domain with Euclidean function d"
]

N_HYP = 1
NEG_Q_INDEX = 1