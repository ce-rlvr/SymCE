import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: I and J are comaximal in R",
    "not Q: The extended ideals are NOT comaximal in the polynomial ring"
]

N_HYP = 4
NEG_Q_INDEX = 4

def extract_witness(witness):
    if isinstance(witness, dict):
        return (witness['elements'], witness['add'], witness['mul'], witness['zero'], witness['I'], witness['J'])
    elif isinstance(witness, tuple):
        if len(witness) == 6:
            return witness
        elif len(witness) == 3:
            R, I, J = witness
            elements = R.elements
            zero = R.zero
            add = R.add if hasattr(R, 'add') else lambda a, b: a + b
            mul = R.mul if hasattr(R, 'mul') else lambda a, b: a * b
            return elements, add, mul, zero, I, J
    
    elements = witness.elements
    zero = witness.zero
    I = witness.I
    J = witness.J
    add = witness.add if hasattr(witness, 'add') else lambda a, b: a + b
    mul = witness.mul if hasattr(witness, 'mul') else lambda a, b: a * b
    return elements, add, mul, zero, I, J

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, I, J = extract_witness(witness)
    except Exception:
        return [False, False, False, False, False]

    def check_H1():
        if zero not in elements: 
            return False
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: 
                return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: 
                return False
            
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                if mul(a, b) != mul(b, a): return False
                
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        return True

    def check_H2():
        if not I: return False
        for i in I:
            if i not in elements: return False
            has_inv = False
            for j in I:
                if add(i, j) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for j in I:
                if add(i, j) not in I: return False
                
            for r in elements:
                if mul(r, i) not in I: return False
        return True

    def check_H3():
        if not J: return False
        for j in J:
            if j not in elements: return False
            has_inv = False
            for k in J:
                if add(j, k) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for k in J:
                if add(j, k) not in J: return False
                
            for r in elements:
                if mul(r, j) not in J: return False
        return True

    def check_H4():
        sums = []
        for i in I:
            for j in J:
                s = add(i, j)
                if s not in sums:
                    sums.append(s)
        for r in elements:
            if r not in sums: return False
        return True

    def check_neg_Q():
        R2 = []
        for a in elements:
            for b in elements:
                p = mul(a, b)
                if p not in R2:
                    R2.append(p)
        
        closure = list(R2)
        added = True
        while added:
            added = False
            new_elements = []
            for x in closure:
                for y in closure:
                    s = add(x, y)
                    if s not in closure and s not in new_elements:
                        new_elements.append(s)
            if new_elements:
                closure.extend(new_elements)
                added = True
        
        for r in elements:
            if r not in closure:
                return True
        return False

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = check_H2()
    except Exception:
        h2 = False

    try:
        h3 = check_H3()
    except Exception:
        h3 = False

    try:
        h4 = check_H4()
    except Exception:
        h4 = False

    try:
        nq = check_neg_Q()
    except Exception:
        nq = False

    return [h1, h2, h3, h4, nq]