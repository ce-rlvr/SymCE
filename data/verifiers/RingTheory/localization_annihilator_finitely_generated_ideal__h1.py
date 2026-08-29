import sympy
from sympy.combinatorics import *
from sympy.matrices import *
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
        # H1: S is a multiplicatively closed subset of R
        R = witness['R']
        S = witness['S']
        mul = witness['mul']
        
        h1 = True
        if not S:
            h1 = False
        else:
            for x in S:
                for y in S:
                    if mul(x, y) not in S:
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    try:
        # H2: I is a finitely generated ideal of R
        I = witness['I']
        add = witness['add']
        zero = witness['zero']
        
        h2 = True
        if not I:
            h2 = False
        else:
            for x in I:
                for y in I:
                    if add(x, y) not in I:
                        h2 = False
                        break
                if not h2: break
            if h2:
                for x in I:
                    for r in R:
                        if mul(r, x) not in I:
                            h2 = False
                            break
                        if mul(x, r) not in I:
                            h2 = False
                            break
                    if not h2: break
    except Exception:
        h2 = False

    try:
        # neg_Q: S^{-1}Ann(I) != Ann_{S^{-1}R}(S^{-1}I)
        S_inv_R = witness['S_inv_R']
        loc_add = witness['loc_add']
        loc_mul = witness['loc_mul']
        loc_zero = witness['loc_zero']
        loc_one = witness['loc_one']
        f = witness['f']
        loc_inv = witness['loc_inv']
        loc_eq = witness.get('loc_eq', lambda x, y: x == y)
        
        is_left_loc = True
        is_right_loc = True
        
        # Check homomorphisms
        for x in R:
            for y in R:
                if not loc_eq(f(add(x, y)), loc_add(f(x), f(y))): 
                    is_left_loc = False
                    is_right_loc = False
                if not loc_eq(f(mul(x, y)), loc_mul(f(x), f(y))): 
                    is_left_loc = False
                    is_right_loc = False
                    
        # Check inverses
        for s in S:
            fs = f(s)
            inv_fs = loc_inv(fs)
            if not loc_eq(loc_mul(fs, inv_fs), loc_one): 
                is_left_loc = False
                is_right_loc = False
            if not loc_eq(loc_mul(inv_fs, fs), loc_one): 
                is_left_loc = False
                is_right_loc = False
                
        # Check element forms
        for x in S_inv_R:
            found_left = False
            found_right = False
            for s in S:
                for r in R:
                    if loc_eq(x, loc_mul(loc_inv(f(s)), f(r))):
                        found_left = True
                    if loc_eq(x, loc_mul(f(r), loc_inv(f(s)))):
                        found_right = True
            if not found_left: is_left_loc = False
            if not found_right: is_right_loc = False
            
        # Check kernels
        for r in R:
            is_zero = loc_eq(f(r), loc_zero)
            has_left_ann = False
            has_right_ann = False
            for s in S:
                if mul(s, r) == zero: has_left_ann = True
                if mul(r, s) == zero: has_right_ann = True
            if is_zero != has_left_ann: is_left_loc = False
            if is_zero != has_right_ann: is_right_loc = False
            
        is_loc = is_left_loc or is_right_loc
        
        if not is_loc:
            neg_q = False
        else:
            # Left annihilator of I
            left_ann_I = []
            for r in R:
                is_ann = True
                for x in I:
                    if mul(r, x) != zero:
                        is_ann = False
                        break
                if is_ann:
                    left_ann_I.append(r)
                    
            # Right annihilator of I
            right_ann_I = []
            for r in R:
                is_ann = True
                for x in I:
                    if mul(x, r) != zero:
                        is_ann = False
                        break
                if is_ann:
                    right_ann_I.append(r)
                    
            def compute_S_inv(subset):
                res = []
                for s in S:
                    for x in subset:
                        if is_left_loc:
                            elem = loc_mul(loc_inv(f(s)), f(x))
                        else:
                            elem = loc_mul(f(x), loc_inv(f(s)))
                        found = False
                        for r in res:
                            if loc_eq(r, elem):
                                found = True
                                break
                        if not found:
                            res.append(elem)
                return res
                
            S_inv_left_ann_I = compute_S_inv(left_ann_I)
            S_inv_right_ann_I = compute_S_inv(right_ann_I)
            S_inv_I = compute_S_inv(I)
            
            left_ann_S_inv_I = []
            for r in S_inv_R:
                is_ann = True
                for x in S_inv_I:
                    if not loc_eq(loc_mul(r, x), loc_zero):
                        is_ann = False
                        break
                if is_ann:
                    left_ann_S_inv_I.append(r)
                    
            right_ann_S_inv_I = []
            for r in S_inv_R:
                is_ann = True
                for x in S_inv_I:
                    if not loc_eq(loc_mul(x, r), loc_zero):
                        is_ann = False
                        break
                if is_ann:
                    right_ann_S_inv_I.append(r)
                    
            def check_eq(set1, set2):
                for x in set1:
                    found = False
                    for y in set2:
                        if loc_eq(x, y):
                            found = True
                            break
                    if not found: return False
                for x in set2:
                    found = False
                    for y in set1:
                        if loc_eq(x, y):
                            found = True
                            break
                    if not found: return False
                return True
                
            left_eq = check_eq(S_inv_left_ann_I, left_ann_S_inv_I)
            right_eq = check_eq(S_inv_right_ann_I, right_ann_S_inv_I)
            
            neg_q = (not left_eq) or (not right_eq)

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is a finitely generated ideal of R",
    "¬Q: S^{-1}(Ann(I)) != Ann_{S^{-1}R}(S^{-1}I)"
]

N_HYP = 2
NEG_Q_INDEX = 2