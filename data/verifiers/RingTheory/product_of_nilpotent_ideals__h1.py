import math
import itertools
import functools
import z3
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: I is a nilpotent ideal of R",
    "H_2: J is a nilpotent ideal of R",
    "¬Q: The product ideal IJ is not nilpotent"
]

def is_zero(val):
    try:
        if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'is_zero') and val.is_zero:
            return True
    except Exception:
        pass
    try:
        from sympy import MatrixBase
        if isinstance(val, MatrixBase):
            return val.is_zero_matrix
    except Exception:
        pass
    try:
        if bool(val == 0):
            return True
    except Exception:
        pass
    return False

def is_nilpotent_ideal(I, R):
    if hasattr(I, 'is_nilpotent_ideal'):
        try:
            return I.is_nilpotent_ideal(R)
        except Exception:
            pass
    if hasattr(R, 'is_nilpotent_ideal'):
        try:
            return R.is_nilpotent_ideal(I)
        except Exception:
            pass
            
    I_list = list(I)
    R_list = list(R)
    
    if not I_list:
        return False
        
    for i in I_list:
        for j in I_list:
            if (i - j) not in I_list:
                return False
            if (i + j) not in I_list:
                return False
        for r in R_list:
            if (i * r) not in I_list:
                return False
            if (r * i) not in I_list:
                return False
                
    powers = {1: list(I_list)}
    max_n = len(I_list) + 3
    
    if all(is_zero(val) for val in I_list):
        return True

    for k in range(2, max_n + 1):
        pk = []
        for j in range(1, k):
            for a in powers[j]:
                for b in powers[k-j]:
                    p = a * b
                    if p not in pk:
                        pk.append(p)
        
        added = True
        while added:
            added = False
            new_elements = []
            for a in pk:
                for b in pk:
                    s = a + b
                    d = a - b
                    if s not in pk and s not in new_elements:
                        new_elements.append(s)
                    if d not in pk and d not in new_elements:
                        new_elements.append(d)
            if new_elements:
                pk.extend(new_elements)
                added = True
                if len(pk) > 1000:
                    break
        powers[k] = pk
        if all(is_zero(val) for val in pk):
            return True
            
    return False

def product_ideal(I, J, R):
    if hasattr(I, 'product_ideal'):
        try:
            return I.product_ideal(J, R)
        except Exception:
            pass
    if hasattr(R, 'product_ideal'):
        try:
            return R.product_ideal(I, J)
        except Exception:
            pass
            
    elements = []
    for i in I:
        for j in J:
            p = i * j
            if p not in elements:
                elements.append(p)
                
    added = True
    while added:
        added = False
        new_elements = []
        for a in elements:
            for b in elements:
                s = a + b
                d = a - b
                if s not in elements and s not in new_elements:
                    new_elements.append(s)
                if d not in elements and d not in new_elements:
                    new_elements.append(d)
            for r in R:
                ar = a * r
                ra = r * a
                if ar not in elements and ar not in new_elements:
                    new_elements.append(ar)
                if ra not in elements and ra not in new_elements:
                    new_elements.append(ra)
        if new_elements:
            elements.extend(new_elements)
            added = True
            if len(elements) > 1000:
                break
    return elements

def conditions(witness):
    try:
        if isinstance(witness, dict):
            I = witness['I']
            J = witness['J']
            R = witness['R']
        elif hasattr(witness, 'I') and hasattr(witness, 'J') and hasattr(witness, 'R'):
            I = witness.I
            J = witness.J
            R = witness.R
        else:
            I, J, R = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_nilpotent_ideal(I, R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_nilpotent_ideal(J, R)
    except Exception:
        h2 = False
        
    try:
        IJ = product_ideal(I, J, R)
        q = is_nilpotent_ideal(IJ, R)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]