import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

class FiniteRing:
    def __init__(self, elements, add_table, mul_table, zero, one):
        self.elements = tuple(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.zero = zero
        self.one = one
        self.elem_to_idx = {e: i for i, e in enumerate(elements)}

    def add(self, a, b):
        return self.add_table[self.elem_to_idx[a]][self.elem_to_idx[b]]

    def mul(self, a, b):
        return self.mul_table[self.elem_to_idx[a]][self.elem_to_idx[b]]

    def is_ring_with_identity(self):
        elements = self.elements
        zero = self.zero
        one = self.one
        if zero not in elements or one not in elements: return False
        
        for a in elements:
            if self.add(a, zero) != a or self.add(zero, a) != a: return False
            
        for a in elements:
            has_inv = False
            for b in elements:
                if self.add(a, b) == zero and self.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for a in elements:
            for b in elements:
                if self.add(a, b) != self.add(b, a): return False
                for c in elements:
                    if self.add(self.add(a, b), c) != self.add(a, self.add(b, c)): return False
                    
        for a in elements:
            if self.mul(a, one) != a or self.mul(one, a) != a: return False
            
        for a in elements:
            for b in elements:
                for c in elements:
                    if self.mul(self.mul(a, b), c) != self.mul(a, self.mul(b, c)): return False
                    
        for a in elements:
            for b in elements:
                for c in elements:
                    if self.mul(a, self.add(b, c)) != self.add(self.mul(a, b), self.mul(a, c)): return False
                    if self.mul(self.add(a, b), c) != self.add(self.mul(a, c), self.mul(b, c)): return False
                    
        return True

    def is_unit(self, u):
        if u not in self.elements: return False
        for v in self.elements:
            if self.mul(u, v) == self.one and self.mul(v, u) == self.one:
                return True
        return False

def make_Zn(n):
    elements = list(range(n))
    add_table = [[(i + j) % n for j in elements] for i in elements]
    mul_table = [[(i * j) % n for j in elements] for i in elements]
    return FiniteRing(elements, add_table, mul_table, 0, 1)

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)

def conditions(witness) -> list[bool]:
    try:
        R, S, f, u = witness
    except Exception:
        return [False, False, False, False]

    def is_ring(ring):
        if hasattr(ring, 'is_ring_with_identity'):
            return ring.is_ring_with_identity()
        if ring in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return True
        if hasattr(ring, 'is_Ring') and ring.is_Ring:
            return hasattr(ring, 'one') and ring.one is not None
        return False

    def is_unit(ring, val):
        if hasattr(ring, 'is_unit'):
            return ring.is_unit(val)
        if ring == sympy.S.Integers:
            return val in (1, -1)
        if ring in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return val != 0
        if hasattr(ring, 'revert'):
            try:
                ring.revert(val)
                return True
            except Exception:
                return False
        return False

    def get_one(ring):
        if hasattr(ring, 'one'):
            return ring.one
        if ring in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return 1
        return 1

    def eval_f(func, val):
        if isinstance(func, (dict, list, tuple)):
            return func[val]
        if hasattr(func, 'subs') and hasattr(func, 'free_symbols'):
            syms = list(func.free_symbols)
            if len(syms) == 1:
                return func.subs(syms[0], val)
            elif len(syms) == 0:
                return func
        return func(val)

    # H1: R and S are rings with identity
    try:
        h1 = bool(is_ring(R) and is_ring(S))
    except Exception:
        h1 = False

    # H2: f maps the identity of R to the identity of S
    try:
        r_one = get_one(R)
        s_one = get_one(S)
        f_one = eval_f(f, r_one)
        h2 = bool(f_one == s_one)
    except Exception:
        h2 = False

    # H3: u is a unit in R
    try:
        h3 = bool(is_unit(R, u))
    except Exception:
        h3 = False

    # neg_Q: f(u) is NOT a unit in S
    try:
        f_u = eval_f(f, u)
        neg_q = not is_unit(S, f_u)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f maps the identity of R to the identity of S",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S"
]

N_HYP = 3
NEG_Q_INDEX = 3