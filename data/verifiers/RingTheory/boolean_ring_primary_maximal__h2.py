import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

class BooleanRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(1 << n))
    def add(self, a, b):
        return a ^ b
    def mul(self, a, b):
        return a & b
    def zero(self):
        return 0
    def one(self):
        return (1 << self.n) - 1
    def __repr__(self):
        return f"BooleanRing({self.n})"

# Top-level setup: named object bindings that the witness expression may reference.
R1 = BooleanRing(1)
R2 = BooleanRing(2)
R3 = BooleanRing(3)
R4 = BooleanRing(4)
R5 = BooleanRing(5)

class RingWrapper:
    def __init__(self, R):
        if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul') and hasattr(R, 'zero') and hasattr(R, 'one'):
            self.elements = list(R.elements)
            self.add = R.add
            self.mul = R.mul
            self.zero = R.zero() if callable(R.zero) else R.zero
            self.one = R.one() if callable(R.one) else R.one
        elif isinstance(R, (list, set, tuple)):
            self.elements = list(R)
            if not self.elements:
                raise ValueError("Empty ring")
            if all(isinstance(x, int) for x in self.elements):
                self.add = lambda a, b: a ^ b
                self.mul = lambda a, b: a & b
                self.zero = 0
                one_val = 0
                for x in self.elements:
                    one_val |= x
                self.one = one_val
            elif all(isinstance(x, (set, frozenset)) for x in self.elements):
                is_set = isinstance(self.elements[0], set)
                self.add = lambda a, b: a ^ b
                self.mul = lambda a, b: a & b
                self.zero = set() if is_set else frozenset()
                one_val = self.zero
                for x in self.elements:
                    one_val = one_val | x
                self.one = one_val
            else:
                raise ValueError("Unsupported ring elements")
        else:
            raise ValueError("Unsupported ring format")

def is_boolean_ring(rw):
    try:
        elements = rw.elements
        zero = rw.zero
        one = rw.one
        if zero not in elements or one not in elements:
            return False
        if zero == one:
            return False
        for x in elements:
            if rw.mul(x, x) != x: return False
            if rw.add(x, zero) != x: return False
            if rw.mul(x, one) != x: return False
            if rw.add(x, x) != zero: return False
            for y in elements:
                if rw.add(x, y) not in elements: return False
                if rw.mul(x, y) not in elements: return False
                if rw.add(x, y) != rw.add(y, x): return False
                if rw.mul(x, y) != rw.mul(y, x): return False
        return True
    except Exception:
        return False

def is_ideal(rw, Q_list):
    try:
        if not Q_list: return False
        if rw.zero not in Q_list: return False
        for x in Q_list:
            if x not in rw.elements: return False
            for y in Q_list:
                if rw.add(x, y) not in Q_list: return False
        for x in Q_list:
            for r in rw.elements:
                if rw.mul(x, r) not in Q_list: return False
        return True
    except Exception:
        return False

def is_maximal_ideal(rw, Q_list):
    try:
        if not is_ideal(rw, Q_list): return False
        if len(Q_list) == len(rw.elements): return False
        
        for y in rw.elements:
            if y not in Q_list:
                gen_ideal_contains_one = False
                for q in Q_list:
                    for r in rw.elements:
                        if rw.add(q, rw.mul(r, y)) == rw.one:
                            gen_ideal_contains_one = True
                            break
                    if gen_ideal_contains_one:
                        break
                if not gen_ideal_contains_one:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            Q = witness.get('Q')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, Q = witness
        else:
            return [False, False]
            
        rw = RingWrapper(R)
        Q_list = list(Q)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_boolean_ring(rw)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_maximal_ideal(rw, Q_list)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: Q is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1