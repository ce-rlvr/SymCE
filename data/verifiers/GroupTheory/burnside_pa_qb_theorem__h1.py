import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
    # H_1: The order of G is p^a q^b for some prime numbers p and q and non-negative integers a and b
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
        elif hasattr(witness, '__len__'):
            order = len(witness)
        else:
            order = -1
            
        if order == -1:
            h1_ok = False
        else:
            order = int(order)
            if order < 1:
                h1_ok = False
            else:
                factors = sympy.ntheory.primefactors(order)
                h1_ok = len(factors) <= 2
    except Exception:
        h1_ok = False

    # ¬Q: G is not a solvable group
    try:
        if hasattr(witness, 'is_solvable'):
            if callable(witness.is_solvable):
                is_solv = bool(witness.is_solvable())
            else:
                is_solv = bool(witness.is_solvable)
        else:
            # If it doesn't have the property, it is not a solvable group
            is_solv = False
    except Exception:
        is_solv = False
        
    neg_q_ok = not is_solv

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is p^a q^b for some prime numbers p and q and non-negative integers a and b",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1