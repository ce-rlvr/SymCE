import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix
import itertools
import functools
import math

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

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def is_reduced_ring(R):
    try:
        from sympy import ZZ, QQ, RR, CC
        if R in (ZZ, QQ, RR, CC):
            return True
        if R.__class__.__name__ in ('Integers', 'Reals', 'Rationals', 'Complexes', 'GaloisField', 'FractionField', 'PolynomialRing'):
            return True
        if hasattr(R, 'is_domain') and R.is_domain:
            return True
        if hasattr(R, 'is_Field') and R.is_Field:
            return True
    except Exception:
        pass

    try:
        R_list = []
        for i, item in enumerate(R):
            if i > 200: return False
            R_list.append(item)
        if not R_list: return False
        
        zero = None
        for z in R_list:
            if all(eq(a + z, a) for a in R_list):
                zero = z
                break
        if zero is None: return False
        
        for a in R_list:
            for b in R_list:
                if not any(eq(a + b, c) for c in R_list): return False
                if not any(eq(a * b, c) for c in R_list): return False
                
        for a in R_list:
            if not any(eq(a + b, zero) for b in R_list): return False
            
        for a in R_list:
            if not eq(a, zero):
                p = a
                for _ in range(len(R_list)):
                    p = p * a
                    if eq(p, zero):
                        return False
        return True
    except Exception:
        return False

def is_in_R(x, R):
    try:
        if hasattr(R, '__contains__'):
            if x in R:
                return True
        if hasattr(R, 'contains'):
            if R.contains(x):
                return True
    except Exception:
        pass
    
    try:
        R_list = []
        for i, item in enumerate(R):
            if i > 200: return False
            R_list.append(item)
        return any(eq(x, r) for r in R_list)
    except Exception:
        return False

def is_two_sided_ideal(L, R):
    try:
        if hasattr(L, 'is_ideal') and L.is_ideal:
            return True
    except Exception:
        pass

    try:
        L_list = list(L)
        if not L_list: return False
        
        R_list = []
        R_is_finite = True
        try:
            for i, item in enumerate(R):
                if i > 200:
                    R_is_finite = False
                    break
                R_list.append(item)
        except TypeError:
            R_is_finite = False
            
        if R_is_finite:
            for y in L_list:
                if not any(eq(y, r) for r in R_list): return False
                
            zero = None
            for z in R_list:
                if all(eq(a + z, a) for a in R_list):
                    zero = z
                    break
            if zero is None: return False
            
            if not any(eq(y, zero) for y in L_list): return False
            
            for a in L_list:
                for b in L_list:
                    if not any(eq(a + b, c) for c in L_list): return False
                    
            for r in R_list:
                for a in L_list:
                    if not any(eq(r * a, c) for c in L_list): return False
                    if not any(eq(a * r, c) for c in L_list): return False
                    
            return True
        else:
            if hasattr(R, '__contains__'):
                for y in L_list:
                    if y not in R: return False
                    
            zero = 0
            if hasattr(R, 'zero'):
                zero = R.zero
                
            if not any(eq(y, zero) for y in L_list): return False
            
            for a in L_list:
                for b in L_list:
                    if not any(eq(a + b, c) for c in L_list): return False
                    
            if all(eq(y, zero) for y in L_list):
                return True
                
            return False
            
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            x = witness.get('x')
            L = witness.get('L')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, x, L = witness
        else:
            R = witness.R
            x = witness.x
            L = witness.L
    except Exception:
        return [False, False, False]

    try:
        h1 = is_reduced_ring(R)
    except Exception:
        h1 = False

    try:
        h2 = is_in_R(x, R)
    except Exception:
        h2 = False

    try:
        neg_q = not is_two_sided_ideal(L, R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: x is an element of R",
    "¬Q: L is not a two-sided ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2