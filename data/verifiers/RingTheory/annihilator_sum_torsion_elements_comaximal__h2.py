import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness elements
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    def get(name, default=None):
        if isinstance(witness, dict):
            return witness.get(name, default)
        return getattr(witness, name, default)

    # H_1: R is a commutative ring
    try:
        R = get('R')
        add = get('add')
        mul = get('mul')
        zero = get('zero')
        one = get('one')
        
        def check_h1():
            if None in (R, add, mul, zero, one): return False
            if zero not in R or one not in R: return False
            for a in R:
                if add(a, zero) != a or add(zero, a) != a: return False
                if mul(a, one) != a or mul(one, a) != a: return False
                has_inv = False
                for b in R:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: return False
                for b in R:
                    if add(a, b) != add(b, a): return False
                    if mul(a, b) != mul(b, a): return False
                    for c in R:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
            return True
            
        h1 = check_h1()
    except Exception:
        h1 = False

    # H_2: x and y are elements of M
    try:
        M = get('M')
        x = get('x')
        y = get('y')
        
        def check_h2():
            if M is None or x is None or y is None: return False
            return x in M and y in M
            
        h2 = check_h2()
    except Exception:
        h2 = False

    # H_3: The annihilator ideals Ann_R(x) and Ann_R(y) are comaximal in R
    try:
        M_zero = get('M_zero')
        action = get('action')
        R = get('R')
        add = get('add')
        mul = get('mul')
        zero = get('zero')
        one = get('one')
        x = get('x')
        y = get('y')
        
        def check_h3():
            if None in (M_zero, action, R, add, mul, zero, one, x, y): return False
            Ann_x = [r for r in R if action(r, x) == M_zero]
            Ann_y = [r for r in R if action(r, y) == M_zero]
            
            def is_ideal(I):
                if zero not in I: return False
                for a in I:
                    has_inv = False
                    for b in I:
                        if add(a, b) == zero:
                            has_inv = True
                            break
                    if not has_inv: return False
                    for b in I:
                        if add(a, b) not in I: return False
                    for r in R:
                        if mul(r, a) not in I: return False
                return True
            
            if not (is_ideal(Ann_x) and is_ideal(Ann_y)): return False
            
            for a in Ann_x:
                for b in Ann_y:
                    if add(a, b) == one:
                        return True
            return False
            
        h3 = check_h3()
    except Exception:
        h3 = False

    # ¬Q: Ann_R(x+y) is not equal to Ann_R(x) ∩ Ann_R(y)
    try:
        M_add = get('M_add')
        M_zero = get('M_zero')
        action = get('action')
        R = get('R')
        x = get('x')
        y = get('y')
        
        def check_neg_q():
            if None in (M_add, M_zero, action, R, x, y): return False
            x_plus_y = M_add(x, y)
            Ann_x = [r for r in R if action(r, x) == M_zero]
            Ann_y = [r for r in R if action(r, y) == M_zero]
            Ann_x_plus_y = [r for r in R if action(r, x_plus_y) == M_zero]
            intersection = [r for r in Ann_x if r in Ann_y]
            
            def sets_equal(A, B):
                for a in A:
                    if a not in B: return False
                for b in B:
                    if b not in A: return False
                return True
            
            return not sets_equal(Ann_x_plus_y, intersection)
            
        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x and y are elements of M",
    "H_3: The annihilator ideals Ann_R(x) and Ann_R(y) are comaximal in R",
    "¬Q: Ann_R(x+y) is not equal to Ann_R(x) ∩ Ann_R(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3