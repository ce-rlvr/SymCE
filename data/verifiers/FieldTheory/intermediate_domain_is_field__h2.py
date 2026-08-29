import sympy
import sympy.combinatorics as comb
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Rational, Integer
import math
import itertools
import functools

# Top-level setup for standard algebraic objects
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a dictionary or a tuple containing:
    (F, D, E, add_op, mul_op, zero, one)
    where F, D, E are finite sets (lists), add_op and mul_op are functions (or dicts/2D lists) 
    defining the field operations, and zero and one are the identity elements.
    """
    try:
        if isinstance(witness, dict):
            F = witness['F']
            D = witness['D']
            E = witness['E']
            add_op = witness['add']
            mul_op = witness['mul']
            zero = witness['zero']
            one = witness['one']
        else:
            F, D, E, add_op, mul_op, zero, one = witness
            
        F = list(F)
        D = list(D)
        E = list(E)
        
        # Limit size to ensure fast verification
        if len(E) > 64:
            return [False, False, False]
            
        def add(a, b):
            if isinstance(add_op, dict): return add_op[(a, b)]
            if isinstance(add_op, list): return add_op[a][b]
            return add_op(a, b)
            
        def mul(a, b):
            if isinstance(mul_op, dict): return mul_op[(a, b)]
            if isinstance(mul_op, list): return mul_op[a][b]
            return mul_op(a, b)
            
        def is_field(S):
            S_list = list(S)
            if zero not in S_list or one not in S_list: 
                return False
            if zero == one: 
                return False
                
            for a in S_list:
                if add(a, zero) != a: return False
                if mul(a, one) != a: return False
                
                has_neg = False
                for b in S_list:
                    if add(a, b) == zero:
                        has_neg = True
                        break
                if not has_neg: return False
                
                if a != zero:
                    has_inv = False
                    for b in S_list:
                        if mul(a, b) == one:
                            has_inv = True
                            break
                    if not has_inv: return False
                    
            for a in S_list:
                for b in S_list:
                    ab_add = add(a, b)
                    ab_mul = mul(a, b)
                    if ab_add not in S_list: return False
                    if ab_mul not in S_list: return False
                    if ab_add != add(b, a): return False
                    if ab_mul != mul(b, a): return False
                    
                    for c in S_list:
                        if add(ab_add, c) != add(a, add(b, c)): return False
                        if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
            return True

        def is_subset(sub, sup):
            return all(x in sup for x in sub)

        # H_1: E/F is a finite field extension
        # Since E is finite, if E and F are fields and F is a subfield of E, it is a finite field extension.
        h1 = is_field(E) and is_field(F) and is_subset(F, E)
        
        # H_2: F is a subset of D and D is a subset of E
        h2 = is_subset(F, D) and is_subset(D, E)
        
        # ¬Q: D is not a field
        neg_q = not is_field(D)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "H_2: F is a subset of D and D is a subset of E",
    "¬Q: D is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2