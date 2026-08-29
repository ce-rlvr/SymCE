import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Helper for finite rings
class ModRingElement:
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
        
    def __add__(self, other):
        if isinstance(other, ModRingElement) and self.mod == other.mod:
            return ModRingElement(self.val + other.val, self.mod)
        return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, ModRingElement) and self.mod == other.mod:
            return ModRingElement(self.val * other.val, self.mod)
        return NotImplemented
        
    def __eq__(self, other):
        if isinstance(other, ModRingElement):
            return self.val == other.val and self.mod == other.mod
        return False
        
    def __hash__(self):
        return hash((self.val, self.mod))
        
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

def Z(n):
    return [ModRingElement(i, n) for i in range(n)]

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    # H1: R is a ring with identity and I is a subset of R
    h1 = False
    try:
        if isinstance(R, list) and isinstance(I, list):
            subset = True
            for x in I:
                if not contains(R, x):
                    subset = False
                    break
            
            if subset:
                is_ring = True
                zero = None
                one = None
                
                for a in R:
                    is_zero = True
                    is_one = True
                    for b in R:
                        try:
                            s = a + b
                            p = a * b
                        except Exception:
                            is_ring = False
                            break
                        if not contains(R, s) or not contains(R, p):
                            is_ring = False
                            break
                        if s != b or b + a != b:
                            is_zero = False
                        if p != b or b * a != b:
                            is_one = False
                    if not is_ring:
                        break
                    if is_zero: zero = a
                    if is_one: one = a
                    
                if is_ring and zero is not None and one is not None:
                    for a in R:
                        has_neg = False
                        for b in R:
                            try:
                                if a + b == zero and b + a == zero:
                                    has_neg = True
                                if a + b != b + a:
                                    is_ring = False
                                for c in R:
                                    if (a + b) + c != a + (b + c):
                                        is_ring = False
                                    if (a * b) * c != a * (b * c):
                                        is_ring = False
                                    if a * (b + c) != a * b + a * c:
                                        is_ring = False
                                    if (a + b) * c != a * c + b * c:
                                        is_ring = False
                            except Exception:
                                is_ring = False
                                break
                        if not has_neg:
                            is_ring = False
                        if not is_ring:
                            break
                    if is_ring:
                        h1 = True
    except Exception:
        h1 = False

    # neg_Q: 1+I is NOT a subgroup of U(R)
    neg_q = False
    try:
        if h1:
            one = None
            for a in R:
                is_one = True
                for b in R:
                    try:
                        if a * b != b or b * a != b:
                            is_one = False
                            break
                    except Exception:
                        is_one = False
                        break
                if is_one:
                    one = a
                    break
            
            if one is not None:
                units = []
                for a in R:
                    is_unit = False
                    for b in R:
                        try:
                            if a * b == one and b * a == one:
                                is_unit = True
                                break
                        except Exception:
                            pass
                    if is_unit:
                        units.append(a)
                        
                one_plus_I = []
                for x in I:
                    try:
                        val = one + x
                        if not contains(one_plus_I, val):
                            one_plus_I.append(val)
                    except Exception:
                        pass
                        
                is_subgroup = True
                for s in one_plus_I:
                    if not contains(units, s):
                        is_subgroup = False
                        break
                
                if is_subgroup:
                    if not contains(one_plus_I, one):
                        is_subgroup = False
                
                if is_subgroup:
                    for a in one_plus_I:
                        for b in one_plus_I:
                            try:
                                if not contains(one_plus_I, a * b):
                                    is_subgroup = False
                                    break
                            except Exception:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                
                if is_subgroup:
                    for a in one_plus_I:
                        inv = None
                        for b in units:
                            try:
                                if a * b == one and b * a == one:
                                    inv = b
                                    break
                            except Exception:
                                pass
                        if inv is None or not contains(one_plus_I, inv):
                            is_subgroup = False
                            break
                            
                neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity and I is a subset of R",
    "¬Q: 1+I is not a subgroup of the group of units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1