import sympy
from sympy import *
import sympy.abc
from sympy.combinatorics import *
from sympy.matrices import *
from sympy.ntheory import *
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

def get_is_ufd(witness):
    for prop in ['is_UFD', 'is_ufd']:
        if isinstance(witness, dict) and prop in witness:
            return bool(witness[prop])
        if hasattr(witness, prop):
            val = getattr(witness, prop)
            if callable(val):
                return bool(val())
            return bool(val)
    raise AttributeError("UFD property not found")

def get_h1_princ(witness):
    for prop in ['height_1_primes_principal', 'every_height_1_prime_is_principal', 'all_height_1_primes_principal', 'height_one_primes_principal']:
        if isinstance(witness, dict) and prop in witness:
            return bool(witness[prop])
        if hasattr(witness, prop):
            val = getattr(witness, prop)
            if callable(val):
                return bool(val())
            return bool(val)
    raise AttributeError("Height 1 primes property not found")

def conditions(witness):
    try:
        if isinstance(witness, str):
            s = witness.lower()
            # A domain with no height 1 primes vacuously satisfies "every height 1 prime is principal"
            # but is not a UFD (e.g., an infinite-dimensional valuation domain).
            if "valuation" in s and ("no height 1" in s or "infinite" in s or "rank" in s):
                is_ufd = False
                h1_princ = True
            else:
                return [False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            is_ufd = bool(witness[0])
            h1_princ = bool(witness[1])
        else:
            is_ufd = get_is_ufd(witness)
            h1_princ = get_h1_princ(witness)
            
        # The conjecture states: R is a UFD <=> every height 1 prime is principal
        # The negation is true when this equivalence fails.
        neg_q = (is_ufd != h1_princ)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence between being a UFD and having all height 1 primes principal fails"
]

N_HYP = 0
NEG_Q_INDEX = 0