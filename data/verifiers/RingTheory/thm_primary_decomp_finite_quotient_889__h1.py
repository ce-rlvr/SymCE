import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    h1, h2, neg_q = False, False, False
    
    # Handle case where witness is a tuple (R, I)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        
        # H1: I is an ideal in R
        try:
            if hasattr(I, 'is_ideal_of'):
                h1 = bool(I.is_ideal_of(R))
            elif hasattr(R, 'is_ideal'):
                h1 = bool(R.is_ideal(I))
            else:
                attr = getattr(I, 'is_ideal', False)
                h1 = bool(attr() if callable(attr) else attr)
        except Exception:
            h1 = False
            
        # H2: The quotient ring R/I is a finite ring
        try:
            if hasattr(R, 'quotient_is_finite'):
                h2 = bool(R.quotient_is_finite(I))
            elif hasattr(I, 'quotient_is_finite'):
                h2 = bool(I.quotient_is_finite(R))
            else:
                attr = getattr(I, 'quotient_is_finite', False)
                h2 = bool(attr() if callable(attr) else attr)
        except Exception:
            h2 = False
            
        # neg_Q: The ideal I does NOT have a primary decomposition in R
        try:
            if hasattr(I, 'has_primary_decomposition_in'):
                has_pd = bool(I.has_primary_decomposition_in(R))
            elif hasattr(R, 'has_primary_decomposition'):
                has_pd = bool(R.has_primary_decomposition(I))
            else:
                attr = getattr(I, 'has_primary_decomposition', True)
                has_pd = bool(attr() if callable(attr) else attr)
            neg_q = not has_pd
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]

    # Handle case where witness is a single object or dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_ideal', False))
        else:
            attr = getattr(witness, 'is_ideal', False)
            h1 = bool(attr() if callable(attr) else attr)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('quotient_is_finite', False))
        else:
            attr = getattr(witness, 'quotient_is_finite', False)
            h2 = bool(attr() if callable(attr) else attr)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            has_pd = bool(witness.get('has_primary_decomposition', True))
        else:
            attr = getattr(witness, 'has_primary_decomposition', True)
            has_pd = bool(attr() if callable(attr) else attr)
        neg_q = not has_pd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal in R",
    "H_2: The quotient ring R/I is a finite ring",
    "¬Q: The ideal I does not have a primary decomposition in R"
]

N_HYP = 2
NEG_Q_INDEX = 2