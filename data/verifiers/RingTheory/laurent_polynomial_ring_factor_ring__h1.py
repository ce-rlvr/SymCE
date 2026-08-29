import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
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

def conditions(witness):
    h1 = True
    h2 = True
    neg_q = False
    
    try:
        has_identity = True
        is_commutative = True
        
        if hasattr(witness, 'has_identity'):
            if witness.has_identity is False:
                has_identity = False
        if hasattr(witness, 'is_commutative'):
            if witness.is_commutative is False:
                is_commutative = False
                
        if isinstance(witness, str):
            s = witness.lower()
            if 'without identity' in s or 'no identity' in s or 'non-unital' in s or 'nonunital' in s:
                has_identity = False
            if '2z' in s or 'nz' in s or 'even' in s:
                has_identity = False
            if 'non-commutative' in s or 'noncommutative' in s:
                is_commutative = False
                
        if isinstance(witness, (int, sympy.Integer)):
            if witness > 1:
                has_identity = False
                
        if not has_identity or not is_commutative:
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The ring of Laurent polynomials over R is defined",
    "H_2: The polynomial ring in two variables over R is defined",
    "¬Q: The Laurent ring is not isomorphic to the factor ring modulo xy - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2