import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            zero_R = witness['zero_R']
            zero_S = witness['zero_S']
            f = witness['f']
            one_R = witness.get('one_R', None)
            one_S = witness.get('one_S', None)
        else:
            R = witness.R
            S = witness.S
            add_R = witness.add_R
            mul_R = witness.mul_R
            add_S = witness.add_S
            mul_S = witness.mul_S
            zero_R = witness.zero_R
            zero_S = witness.zero_S
            f = witness.f
            one_R = getattr(witness, 'one_R', None)
            one_S = getattr(witness, 'one_S', None)

        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f

        h1 = True
        for x in R:
            for y in R:
                if f_func(add_R(x, y)) != add_S(f_func(x), f_func(y)):
                    h1 = False
                if f_func(mul_R(x, y)) != mul_S(f_func(x), f_func(y)):
                    h1 = False
        
        if one_R is not None and one_S is not None:
            if f_func(one_R) != one_S:
                h1 = False

    except Exception:
        h1 = False

    try:
        is_injective = True
        R_list = list(R)
        for i in range(len(R_list)):
            for j in range(i + 1, len(R_list)):
                if f_func(R_list[i]) == f_func(R_list[j]):
                    is_injective = False
                    break
            if not is_injective:
                break
        
        ker = [x for x in R_list if f_func(x) == zero_S]
        
        ker_is_trivial = True
        has_zero = False
        for x in ker:
            if x == zero_R:
                has_zero = True
            else:
                ker_is_trivial = False
        if not has_zero:
            ker_is_trivial = False
            
        neg_q = (is_injective != ker_is_trivial)
        
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "¬Q: f is injective XOR ker(f) == {0_R}"
]

N_HYP = 1
NEG_Q_INDEX = 1