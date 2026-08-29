import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        R = witness.get('R', [])
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        one = witness.get('one')
        
        M = witness.get('M', [])
        m_add = witness.get('m_add')
        rmul = witness.get('rmul')
        m_zero = witness.get('m_zero')
        
        I = witness.get('I', [])
    except Exception:
        return [False, False, False]

    def check_H1():
        try:
            if not R: return False
            if zero not in R or one not in R: return False
            for a in R:
                if add(a, zero) != a or add(zero, a) != a: return False
                if mul(a, one) != a or mul(one, a) != a: return False
                if mul(a, zero) != zero or mul(zero, a) != zero: return False
                has_inv = False
                for b in R:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: return False
                for b in R:
                    if add(a, b) != add(b, a): return False
                    for c in R:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            if not M: return False
            if m_zero not in M: return False
            for m in M:
                if m_add(m, m_zero) != m or m_add(m_zero, m) != m: return False
                if rmul(one, m) != m: return False
                if rmul(zero, m) != m_zero: return False
                has_inv = False
                for n in M:
                    if m_add(m, n) == m_zero and m_add(n, m) == m_zero:
                        has_inv = True
                        break
                if not has_inv: return False
                for n in M:
                    if m_add(m, n) != m_add(n, m): return False
                    for p in M:
                        if m_add(m_add(m, n), p) != m_add(m, m_add(n, p)): return False
            
            for r in R:
                for m in M:
                    if rmul(r, m) not in M: return False
                    for n in M:
                        if rmul(r, m_add(m, n)) != m_add(rmul(r, m), rmul(r, n)): return False
                for s in R:
                    for m in M:
                        if rmul(add(r, s), m) != m_add(rmul(r, m), rmul(s, m)): return False
                        if rmul(mul(r, s), m) != rmul(r, rmul(s, m)): return False
            return True
        except Exception:
            return False

    def check_neg_Q():
        try:
            if not I:
                return True
                
            for i in I:
                if i not in R:
                    return True
            
            is_left_ideal = True
            for i in I:
                for r in R:
                    if mul(r, i) not in I:
                        is_left_ideal = False
                        break
                if not is_left_ideal: break
                
            for i in I:
                for j in I:
                    if add(i, j) not in I:
                        is_left_ideal = False
                        break
                if not is_left_ideal: break
                
            N = []
            for m in M:
                im_is_zero = True
                for i in I:
                    if rmul(i, m) != m_zero:
                        im_is_zero = False
                        break
                if im_is_zero:
                    N.append(m)
                    
            is_submodule = True
            for n in N:
                for r in R:
                    if rmul(r, n) not in N:
                        is_submodule = False
                        break
                if not is_submodule: break
                
            return not (is_left_ideal and is_submodule)
        except Exception:
            return False

    return [check_H1(), check_H2(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is a left R-module",
    "¬Q: The conclusion fails (either R/I is not a left R-module or N is not a submodule)"
]

N_HYP = 2
NEG_Q_INDEX = 2