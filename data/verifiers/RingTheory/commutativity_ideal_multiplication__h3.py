import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def is_commutative_ring(R):
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring:
            if hasattr(R, 'is_commutative'):
                return bool(R.is_commutative)
            return True
    except Exception:
        pass

    try:
        R_list = []
        for i, x in enumerate(R):
            if i > 1000:
                return False
            R_list.append(x)
            
        if not R_list: 
            return False
        
        for a in R_list:
            for b in R_list:
                if a * b != b * a:
                    return False
                    
        for a in R_list:
            for b in R_list:
                if a + b not in R_list: return False
                if a * b not in R_list: return False
                
        has_zero = False
        for z in R_list:
            if all(a + z == a for a in R_list):
                has_zero = True
                all_inv = True
                for a in R_list:
                    if not any(a + b == z for b in R_list):
                        all_inv = False
                        break
                if all_inv:
                    break
        if not has_zero: 
            return False
        
        for a in R_list:
            for b in R_list:
                for c in R_list:
                    if (a * b) * c != a * (b * c): return False
                    if (a + b) + c != a + (b + c): return False
                    if a * (b + c) != a * b + a * c: return False
                    
        return True
    except Exception:
        pass
    return False

def is_ideal(I, R):
    try:
        if hasattr(I, 'is_ideal'):
            if callable(I.is_ideal):
                return bool(I.is_ideal(R))
            return bool(I.is_ideal)
    except Exception:
        pass

    try:
        I_list = []
        for i, x in enumerate(I):
            if i > 1000:
                return False
            I_list.append(x)
            
        R_list = []
        for i, x in enumerate(R):
            if i > 1000:
                return False
            R_list.append(x)
            
        if not I_list: 
            return False
        
        for i in I_list:
            if i not in R_list: return False
            
        for a in I_list:
            for b in I_list:
                if a + b not in I_list: return False
                
        for i in I_list:
            for r in R_list:
                if i * r not in I_list: return False
                if r * i not in I_list: return False
                
        return True
    except Exception:
        pass
    return False

def check_IJ_eq_JI(I, J, R):
    try:
        if hasattr(I, '__mul__') and hasattr(J, '__mul__'):
            if not isinstance(I, (list, tuple, set)) and not isinstance(J, (list, tuple, set)):
                return I * J == J * I
    except Exception:
        pass

    try:
        I_list = []
        for i, x in enumerate(I):
            if i > 1000: return None
            I_list.append(x)
            
        J_list = []
        for i, x in enumerate(J):
            if i > 1000: return None
            J_list.append(x)
        
        def ideal_product(A, B):
            prods = []
            for a in A:
                for b in B:
                    prods.append(a * b)
            
            closure = []
            for p in prods:
                if p not in closure:
                    closure.append(p)
                    
            added = True
            while added:
                if len(closure) > 500:
                    return None
                added = False
                new_elements = []
                for x in closure:
                    for y in closure:
                        s = x + y
                        if s not in closure and s not in new_elements:
                            new_elements.append(s)
                            if len(closure) + len(new_elements) > 500:
                                return None
                if new_elements:
                    closure.extend(new_elements)
                    added = True
            return closure
            
        IJ = ideal_product(I_list, J_list)
        if IJ is None: return None
        
        JI = ideal_product(J_list, I_list)
        if JI is None: return None
        
        for x in IJ:
            if x not in JI: return False
        for x in JI:
            if x not in IJ: return False
            
        return True
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, I, J = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(I, R)
    except Exception:
        h2 = False
        
    try:
        q = check_IJ_eq_JI(I, J, R)
        if q is None:
            neg_q = False
        else:
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: IJ != JI"
]

N_HYP = 2
NEG_Q_INDEX = 2