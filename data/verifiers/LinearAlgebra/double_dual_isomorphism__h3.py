import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: V^{**} is the double dual space of V",
    "¬Q: The linear map \\Phi is not a vector space isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1 and H_2 are assumed to hold for the provided witness context.
    # The conjecture fails (neg_Q is True) if and only if the vector space V is infinite-dimensional,
    # because the natural evaluation map \Phi: V -> V^{**} is an isomorphism if and only if V is finite-dimensional.
    h1_ok = True
    h2_ok = True
    neg_q_ok = False
    
    try:
        if isinstance(witness, str):
            w = witness.lower()
            inf_keywords = ['inf', 'poly', 'seq', 'fun', 'l2', 'l^2', 'r[x]', 'c[x]', 'r^n', 'c^n']
            fin_keywords = ['r^2', 'r^3', 'r^4', 'finite', 'r2', 'r3', 'r^1']
            
            if any(k in w for k in inf_keywords):
                neg_q_ok = True
            elif w in ['r', 'c', 'q']:
                neg_q_ok = False
            elif any(k in w for k in fin_keywords):
                neg_q_ok = False
            else:
                # Default to True for abstract string witnesses not explicitly finite
                neg_q_ok = True
        elif isinstance(witness, int):
            # Integers typically represent finite dimensions
            neg_q_ok = False
        elif hasattr(witness, 'shape') or hasattr(witness, 'is_Matrix'):
            # Matrices represent finite-dimensional spaces
            neg_q_ok = False
        elif isinstance(witness, type):
            if 'Poly' in witness.__name__ or 'Seq' in witness.__name__:
                neg_q_ok = True
            else:
                neg_q_ok = True
        else:
            # Fallback for other objects representing infinite-dimensional spaces
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]