import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: {S_alpha} is a family of rings",
    "H_3: {f_alpha} is a family of ring homomorphisms",
    "¬Q: The kernel of the induced homomorphism f is not the intersection of ker(f_alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        R, S_list, f_list = witness
    except Exception:
        return [False, False, False, False]
        
    def check_ring(ring_tuple):
        try:
            elems, add, mul, zero = ring_tuple
            elems = list(elems)
            if zero not in elems: return False
            
            def _add(a, b): return add(a, b) if callable(add) else add[(a, b)]
            def _mul(a, b): return mul(a, b) if callable(mul) else mul[(a, b)]
            
            for a in elems:
                for b in elems:
                    if _add(a, b) not in elems: return False
                    if _mul(a, b) not in elems: return False
            
            for a in elems:
                if _add(a, zero) != a or _add(zero, a) != a: return False
                has_inv = False
                for b in elems:
                    if _add(a, b) == zero and _add(b, a) == zero:
                        has_inv = True
                if not has_inv: return False
                
                for b in elems:
                    if _add(a, b) != _add(b, a): return False
                    for c in elems:
                        if _add(_add(a, b), c) != _add(a, _add(b, c)): return False
                        
            for a in elems:
                for b in elems:
                    for c in elems:
                        if _mul(_mul(a, b), c) != _mul(a, _mul(b, c)): return False
                        if _mul(a, _add(b, c)) != _add(_mul(a, b), _mul(a, c)): return False
                        if _mul(_add(a, b), c) != _add(_mul(a, c), _mul(b, c)): return False
                        
            has_id = False
            for e in elems:
                if all(_mul(e, a) == a and _mul(a, e) == a for a in elems):
                    has_id = True
                    break
            if not has_id: return False
            
            return True
        except Exception:
            return False

    # H1: R is a ring
    h1 = check_ring(R)
    
    # H2: S_list is a family of rings
    try:
        h2 = all(check_ring(S) for S in S_list)
    except Exception:
        h2 = False
        
    # H3: f_list is a family of ring homomorphisms
    def check_hom(R, S, f):
        try:
            R_elems, R_add, R_mul, R_zero = R
            S_elems, S_add, S_mul, S_zero = S
            
            def _r_add(a, b): return R_add(a, b) if callable(R_add) else R_add[(a, b)]
            def _r_mul(a, b): return R_mul(a, b) if callable(R_mul) else R_mul[(a, b)]
            def _s_add(a, b): return S_add(a, b) if callable(S_add) else S_add[(a, b)]
            def _s_mul(a, b): return S_mul(a, b) if callable(S_mul) else S_mul[(a, b)]
            def _f(a): return f(a) if callable(f) else f[a]
            
            R_id = next(e for e in R_elems if all(_r_mul(e, a) == a and _r_mul(a, e) == a for a in R_elems))
            S_id = next(e for e in S_elems if all(_s_mul(e, a) == a and _s_mul(a, e) == a for a in S_elems))
            
            if _f(R_id) != S_id: return False
            
            for a in R_elems:
                if _f(a) not in S_elems: return False
                for b in R_elems:
                    if _f(_r_add(a, b)) != _s_add(_f(a), _f(b)): return False
                    if _f(_r_mul(a, b)) != _s_mul(_f(a), _f(b)): return False
            return True
        except Exception:
            return False

    try:
        if len(S_list) != len(f_list):
            h3 = False
        else:
            h3 = all(check_hom(R, S_list[i], f_list[i]) for i in range(len(S_list)))
    except Exception:
        h3 = False
        
    # neg_Q: The kernel of the induced homomorphism f is NOT the intersection of ker(f_alpha)
    try:
        R_elems = list(R[0])
        kers = []
        for i in range(len(S_list)):
            S_zero = S_list[i][3]
            f = f_list[i]
            def _f(a, f=f): return f(a) if callable(f) else f[a]
            ker = [x for x in R_elems if _f(x) == S_zero]
            kers.append(ker)
            
        if not kers:
            intersection = []
        else:
            intersection = kers[0]
            for k in kers[1:]:
                intersection = [x for x in intersection if x in k]
                
        ker_f = []
        for x in R_elems:
            is_zero = True
            for i in range(len(S_list)):
                S_zero = S_list[i][3]
                f = f_list[i]
                def _f(a, f=f): return f(a) if callable(f) else f[a]
                if _f(x) != S_zero:
                    is_zero = False
                    break
            if is_zero:
                ker_f.append(x)
                
        def same_elements(l1, l2):
            for x in l1:
                if x not in l2: return False
            for x in l2:
                if x not in l1: return False
            return True
            
        neg_q = not same_elements(ker_f, intersection)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]