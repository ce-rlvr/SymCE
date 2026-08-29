import itertools
import math
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False] * 4 + [False]
        R, I, J = witness
        if not isinstance(R, (list, tuple, set)):
            return [False] * 4 + [False]
        R = list(R)
        I = list(I)
        J = list(J)
    except Exception:
        return [False] * 4 + [False]

    if not R:
        return [False] * 4 + [False]

    def eq(a, b):
        try:
            res = (a == b)
            if isinstance(res, bool):
                return res
            try:
                return bool(res)
            except Exception:
                return res.all()
        except Exception:
            return False

    def in_list(a, lst):
        for x in lst:
            if eq(a, x):
                return True
        return False

    try:
        zeros_list = []
        for z in R:
            if all(in_list(z + r, R) and eq(z + r, r) for r in R):
                zeros_list.append(z)
        if not zeros_list:
            zero = None
        else:
            zero = zeros_list[0]
    except Exception:
        zero = None

    def is_ring(A):
        if zero is None: return False
        for a in A:
            for b in A:
                if not in_list(a + b, A): return False
                if not in_list(a * b, A): return False
                if not in_list(a - b, A): return False
                if not eq(a + b, b + a): return False
        if len(A) <= 30:
            for a in A:
                for b in A:
                    for c in A:
                        if not eq((a * b) * c, a * (b * c)): return False
                        if not eq(a * (b + c), a * b + a * c): return False
                        if not eq((a + b) * c, a * c + b * c): return False
        return True

    def is_ideal(A):
        if not is_ring(R): return False
        if not A: return False
        for a in A:
            if not in_list(a, R): return False
        for a in A:
            for b in A:
                if not in_list(a - b, A): return False
        for a in A:
            for r in R:
                if not in_list(r * a, A): return False
                if not in_list(a * r, A): return False
        return True

    def has_regular(A):
        if zero is None: return False
        for a in A:
            is_reg = True
            for r in R:
                if not eq(r, zero):
                    if eq(a * r, zero) or eq(r * a, zero):
                        is_reg = False
                        break
            if is_reg:
                return True
        return False

    try:
        h1 = is_ideal(I)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(J)
    except Exception:
        h2 = False

    try:
        h3 = has_regular(I)
    except Exception:
        h3 = False

    try:
        h4 = has_regular(J)
    except Exception:
        h4 = False

    try:
        if zero is None:
            neg_q = False
        else:
            closure = []
            for a in I:
                for b in J:
                    p = a * b
                    if not in_list(p, closure):
                        closure.append(p)
            
            changed = True
            while changed:
                changed = False
                n = len(closure)
                for i in range(n):
                    for j in range(n):
                        s = closure[i] + closure[j]
                        if not in_list(s, closure):
                            closure.append(s)
                            changed = True
                        d = closure[i] - closure[j]
                        if not in_list(d, closure):
                            closure.append(d)
                            changed = True
                if len(closure) > len(R):
                    break
            
            neg_q = not has_regular(closure)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: I contains at least one regular element",
    "H_4: J contains at least one regular element",
    "¬Q: The product ideal IJ contains no regular element"
]

N_HYP = 4
NEG_Q_INDEX = 4