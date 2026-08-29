import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.combinatorics
import sympy.combinatorics.permutations
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

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is a proper ideal of R",
    "¬Q: There do not exist prime ideals P_1, ..., P_n containing I such that P_1 ... P_n is contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_prop(obj, names):
    for name in names:
        if hasattr(obj, name):
            attr = getattr(obj, name)
            return bool(attr() if callable(attr) else attr)
        if isinstance(obj, dict) and name in obj:
            attr = obj[name]
            return bool(attr() if callable(attr) else attr)
    raise ValueError(f"None of {names} found on {obj}")

def conditions(witness):
    if callable(witness) and not isinstance(witness, type):
        try:
            witness = witness()
        except Exception:
            pass
    elif isinstance(witness, type):
        try:
            witness = witness()
        except Exception:
            pass

    h1, h2, neg_q = False, False, False
    
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        if isinstance(R, type):
            try: R = R()
            except Exception: pass
        if isinstance(I, type):
            try: I = I()
            except Exception: pass
            
        try:
            h1 = check_prop(R, ['is_Noetherian', 'is_noetherian', 'noetherian'])
        except Exception:
            try:
                h1 = check_prop(witness, ['is_Noetherian', 'is_noetherian', 'noetherian'])
            except Exception:
                h1 = False
                
        try:
            h2 = check_prop(I, ['is_proper_ideal', 'is_proper', 'proper_ideal'])
        except Exception:
            try:
                h2 = check_prop(witness, ['is_proper_ideal', 'is_proper', 'proper_ideal'])
            except Exception:
                h2 = False
                
        try:
            q = check_prop(I, ['contains_product_of_primes', 'has_product_of_primes', 'conclusion'])
            neg_q = not q
        except Exception:
            try:
                q = check_prop(R, ['contains_product_of_primes', 'has_product_of_primes', 'conclusion'])
                neg_q = not q
            except Exception:
                try:
                    q = check_prop(witness, ['contains_product_of_primes', 'has_product_of_primes', 'conclusion'])
                    neg_q = not q
                except Exception:
                    neg_q = False
                
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]

    try:
        h1 = check_prop(witness, ['is_Noetherian', 'is_noetherian', 'noetherian', 'R_is_Noetherian'])
    except Exception:
        h1 = False

    try:
        h2 = check_prop(witness, ['is_proper_ideal', 'is_proper', 'proper_ideal', 'I_is_proper'])
    except Exception:
        h2 = False

    try:
        q = check_prop(witness, [
            'contains_product_of_primes',
            'has_product_of_primes',
            'contains_product_of_primes_containing_it',
            'product_of_primes_contained',
            'conclusion'
        ])
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]