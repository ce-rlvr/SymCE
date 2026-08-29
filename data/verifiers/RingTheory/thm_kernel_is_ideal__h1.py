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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism",
    "¬Q: ker(f) is not a two-sided ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        def get_val(obj, key):
            if isinstance(obj, dict):
                return obj[key]
            return getattr(obj, key)

        R = list(get_val(witness, 'R'))
        S = list(get_val(witness, 'S'))
        add_R = get_val(witness, 'add_R')
        mul_R = get_val(witness, 'mul_R')
        add_S = get_val(witness, 'add_S')
        mul_S = get_val(witness, 'mul_S')
        zero_R = get_val(witness, 'zero_R')
        zero_S = get_val(witness, 'zero_S')
        f_val = get_val(witness, 'f')
        
        if isinstance(f_val, dict):
            f = lambda x: f_val[x]
        else:
            f = f_val

        # H_1: f is a ring homomorphism
        h1 = True
        for x in R:
            for y in R:
                if f(add_R(x, y)) != add_S(f(x), f(y)):
                    h1 = False
                if f(mul_R(x, y)) != mul_S(f(x), f(y)):
                    h1 = False

        # neg_Q: ker(f) is not a two-sided ideal of R
        ker = [x for x in R if f(x) == zero_S]
        
        is_ideal = True
        
        # 1. Must contain the zero element of R
        if zero_R not in ker:
            is_ideal = False
            
        # 2. Must be closed under addition
        for k1 in ker:
            for k2 in ker:
                if add_R(k1, k2) not in ker:
                    is_ideal = False
                    
        # 3. Must contain additive inverses
        for k in ker:
            has_inv = False
            for x in ker:
                if add_R(k, x) == zero_R and add_R(x, k) == zero_R:
                    has_inv = True
                    break
            if not has_inv:
                is_ideal = False
                
        # 4. Must be closed under left and right multiplication by any element in R
        for k in ker:
            for r in R:
                if mul_R(r, k) not in ker:
                    is_ideal = False
                if mul_R(k, r) not in ker:
                    is_ideal = False
                    
        neg_q = not is_ideal
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]