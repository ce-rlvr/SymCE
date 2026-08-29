import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_prop(obj, prop_names, default=False):
    try:
        for prop in prop_names:
            if isinstance(obj, dict) and prop in obj:
                val = obj[prop]
                return bool(val() if callable(val) else val)
            if hasattr(obj, prop):
                val = getattr(obj, prop)
                return bool(val() if callable(val) else val)
    except Exception:
        pass
    return default

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            h1 = extract_prop(R, ['is_commutative_ring', 'is_commutative'])
            h2 = extract_prop(I, ['is_maximal_non_fg', 'is_maximal_non_finitely_generated', 'maximal_non_fg'])
            q = extract_prop(I, ['is_prime', 'is_prime_ideal'])
        else:
            h1 = extract_prop(witness, ['is_commutative_ring', 'is_commutative'])
            h2 = extract_prop(witness, ['is_maximal_non_fg', 'is_maximal_non_finitely_generated', 'maximal_non_fg'])
            q = extract_prop(witness, ['is_prime', 'is_prime_ideal'])
        
        return [h1, h2, not q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is maximal with respect to the property of not being finitely generated",
    "¬Q: I is not a prime ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2