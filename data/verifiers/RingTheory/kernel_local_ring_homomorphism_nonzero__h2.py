import sympy
from sympy import Rational, Integer
import math
import itertools
import functools

class Z_n:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def __repr__(self):
        return f"Z_{self.n}"

Z1 = Z_n(1)
Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z6 = Z_n(6)
Z8 = Z_n(8)

def is_valid_ring(R):
    try:
        if not hasattr(R, 'elements') or not hasattr(R, 'add') or not hasattr(R, 'mul'):
            return False
        if not hasattr(R, 'zero') or not hasattr(R, 'one'):
            return False
        elements = list(R.elements)
        if R.zero not in elements or R.one not in elements:
            return False
        for a in elements:
            if R.add(a, R.zero) != a or R.add(R.zero, a) != a:
                return False
            has_inv = False
            for b in elements:
                if R.add(a, b) == R.zero and R.add(b, a) == R.zero:
                    has_inv = True
                    break
            if not has_inv:
                return False
            for b in elements:
                if R.add(a, b) != R.add(b, a):
                    return False
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)):
                        return False
        for a in elements:
            if R.mul(a, R.one) != a or R.mul(R.one, a) != a:
                return False
            for b in elements:
                for c in elements:
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)):
                        return False
        for a in elements:
            for b in elements:
                for c in elements:
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)):
                        return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)):
                        return False
        return True
    except Exception:
        return False

def is_ideal(R, I):
    try:
        I_list = list(I)
        if not I_list: 
            return False
        elements = list(R.elements)
        for x in I_list:
            if x not in elements:
                return False
        for a in I_list:
            for b in I_list:
                minus_b = None
                for x in elements:
                    if R.add(b, x) == R.zero and R.add(x, b) == R.zero:
                        minus_b = x
                        break
                if minus_b is None:
                    return False
                if R.add(a, minus_b) not in I_list:
                    return False
        for r in elements:
            for x in I_list:
                if R.mul(r, x) not in I_list: return False
                if R.mul(x, r) not in I_list: return False
        return True
    except Exception:
        return False

def is_unique_maximal_ideal(R, M):
    try:
        if not is_valid_ring(R):
            return False
        if not is_ideal(R, M):
            return False
        M_list = list(M)
        if R.one in M_list:
            return False
        elements = list(R.elements)
        for x in elements:
            if x not in M_list:
                is_unit = False
                for y in elements:
                    if R.mul(x, y) == R.one and R.mul(y, x) == R.one:
                        is_unit = True
                        break
                if not is_unit:
                    return False
        return True
    except Exception:
        return False

def is_ring_homomorphism(R, S, f):
    try:
        if not is_valid_ring(R) or not is_valid_ring(S):
            return False
        elements_R = list(R.elements)
        elements_S = list(S.elements)
        for x in elements_R:
            fx = f[x] if isinstance(f, dict) else f(x)
            if fx not in elements_S:
                return False
                
        for a in elements_R:
            for b in elements_R:
                ab = R.add(a, b)
                fa = f[a] if isinstance(f, dict) else f(a)
                fb = f[b] if isinstance(f, dict) else f(b)
                fab = f[ab] if isinstance(f, dict) else f(ab)
                if fab != S.add(fa, fb):
                    return False
                    
        for a in elements_R:
            for b in elements_R:
                ab = R.mul(a, b)
                fa = f[a] if isinstance(f, dict) else f(a)
                fb = f[b] if isinstance(f, dict) else f(b)
                fab = f[ab] if isinstance(f, dict) else f(ab)
                if fab != S.mul(fa, fb):
                    return False
                    
        f1 = f[R.one] if isinstance(f, dict) else f(R.one)
        if f1 != S.one:
            return False
            
        return True
    except Exception:
        return False

def neg_conclusion(R, S, M, f):
    try:
        elements_R = list(R.elements)
        M_list = list(M)
        ker = []
        for x in elements_R:
            fx = f[x] if isinstance(f, dict) else f(x)
            if fx == S.zero:
                ker.append(x)
                
        for x in ker:
            if x not in M_list:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        R = witness['R']
        M = witness['M']
        S = witness['S']
        f = witness['f']
    except Exception:
        return [False, False, False]
        
    h1 = is_unique_maximal_ideal(R, M)
    h2 = is_ring_homomorphism(R, S, f)
    neg_q = neg_conclusion(R, S, M, f)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with unique maximal ideal M",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: The kernel of f is not a subset of M"
]

N_HYP = 2
NEG_Q_INDEX = 2