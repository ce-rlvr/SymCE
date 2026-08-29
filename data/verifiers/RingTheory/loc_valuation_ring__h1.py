import sympy
from sympy import *
from sympy.abc import *
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a valuation ring",
    "H_2: P is a prime ideal of R",
    "¬Q: The localized ring R_P is not a valuation ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    Since standard SymPy domains (integral domains) always satisfy the conclusion 
    if they satisfy the hypotheses, a true counterexample must be a more complex 
    structure (e.g., a Manis valuation ring with zero divisors that is not a Prüfer ring).
    We use duck typing to evaluate the properties of the provided witness.
    """
    h1 = False
    h2 = False
    neg_q = False

    # 1. If witness is a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_valuation_ring', False))
            h2 = bool(witness.get('is_prime_ideal', False))
            neg_q = not bool(witness.get('localization_is_valuation_ring', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. If witness is an object with properties/methods
    try:
        if hasattr(witness, 'is_valuation_ring'):
            attr = witness.is_valuation_ring
            h1 = attr() if callable(attr) else bool(attr)
            
            attr2 = getattr(witness, 'is_prime_ideal', False)
            h2 = attr2() if callable(attr2) else bool(attr2)
            
            attr3 = getattr(witness, 'localization_is_valuation_ring', True)
            q = attr3() if callable(attr3) else bool(attr3)
            neg_q = not q
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. If witness is a tuple (R, P)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, P = witness
        try:
            attr = getattr(R, 'is_valuation_ring', False)
            h1 = attr() if callable(attr) else bool(attr)
        except Exception:
            h1 = False
            
        try:
            attr2 = getattr(P, 'is_prime_ideal', False)
            if callable(attr2):
                try:
                    h2 = attr2(R)
                except Exception:
                    h2 = attr2()
            else:
                h2 = bool(attr2)
        except Exception:
            h2 = False
            
        try:
            if hasattr(R, 'localization'):
                loc = R.localization(P)
            elif hasattr(R, 'localize'):
                loc = R.localize(P)
            else:
                loc = None
                
            if loc is not None:
                attr3 = getattr(loc, 'is_valuation_ring', True)
                q = attr3() if callable(attr3) else bool(attr3)
                neg_q = not q
            else:
                attr3 = getattr(R, 'localization_is_valuation_ring', True)
                if callable(attr3):
                    try:
                        q = attr3(P)
                    except Exception:
                        q = attr3()
                else:
                    q = bool(attr3)
                neg_q = not q
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]