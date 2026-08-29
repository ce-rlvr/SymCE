import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: G_1, G_2, and K are groups",
    "H_2: f_1: K -> G_1 is a group homomorphism",
    "H_3: f_2: K -> G_2 is a group homomorphism",
    "¬Q: There does not exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2"
]

def is_group(G):
    return isinstance(G, PermutationGroup)

def make_callable(K, G, f):
    if callable(f):
        return f
    if isinstance(f, dict):
        return lambda x: f.get(x, None)
    return lambda x: None

def is_homomorphism(K, G, f_callable):
    try:
        elements = list(K.generate())
        for x in elements:
            if f_callable(x) not in G:
                return False
        for x in elements:
            for y in elements:
                if f_callable(x * y) != f_callable(x) * f_callable(y):
                    return False
        return True
    except Exception:
        return False

def conclusion_holds(K, G1, G2, f1_callable, f2_callable):
    try:
        elements = list(K.generate())
        for x in elements:
            if f1_callable(x) not in G1 or f2_callable(x) not in G2:
                return False
        for x in elements:
            for y in elements:
                fx1 = f1_callable(x)
                fx2 = f2_callable(x)
                fy1 = f1_callable(y)
                fy2 = f2_callable(y)
                fxy1 = f1_callable(x * y)
                fxy2 = f2_callable(x * y)
                
                # In the direct product G1 x G2, the group operation is component-wise.
                # The unique function f satisfying the projections must be f(x) = (f1(x), f2(x)).
                # We check if this f is a valid group homomorphism.
                if fxy1 != fx1 * fy1 or fxy2 != fx2 * fy2:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        K, G1, G2, f1, f2 = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = is_group(K) and is_group(G1) and is_group(G2)
    except Exception:
        h1 = False
        
    if not h1:
        return [False, False, False, False]
        
    try:
        f1_callable = make_callable(K, G1, f1)
        h2 = is_homomorphism(K, G1, f1_callable)
    except Exception:
        h2 = False
        
    try:
        f2_callable = make_callable(K, G2, f2)
        h3 = is_homomorphism(K, G2, f2_callable)
    except Exception:
        h3 = False
        
    try:
        q = conclusion_holds(K, G1, G2, f1_callable, f2_callable)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]