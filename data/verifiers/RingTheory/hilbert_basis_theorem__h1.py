import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

class EvenIntegersRing:
    """
    Represents the ring of even integers (2Z).
    It is a Noetherian ring, but its polynomial ring is not Noetherian.
    """
    @property
    def is_noetherian(self):
        return True
    
    @property
    def is_polynomial_ring_noetherian(self):
        return False
        
    def __str__(self):
        return "2Z"

class ZeroMultiplicationRing:
    """
    Represents a finite abelian group equipped with zero multiplication.
    It is Noetherian (satisfies ACC on subgroups), but the polynomial ring has zero multiplication
    and is an infinite direct sum, hence not Noetherian.
    """
    @property
    def is_noetherian(self):
        return True
        
    @property
    def is_polynomial_ring_noetherian(self):
        return False
        
    def __str__(self):
        return "Zero multiplication ring"

# Bindings for potential witness expressions
EvenIntegers = EvenIntegersRing()
TwoZ = EvenIntegersRing()
ZeroMultRing = ZeroMultiplicationRing()

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check H_1: R is a Noetherian ring
    try:
        if isinstance(witness, str):
            s = witness.lower().strip()
            if s in ["2z", "2zz", "even integers", "ring of even integers"]:
                h1 = True
            elif "zero mult" in s or "zero-mult" in s:
                h1 = True
            elif "without identity" in s or "non-unital" in s or "nonunital" in s:
                h1 = True
            elif s in ["z", "zz", "integers", "q", "qq", "rationals"]:
                h1 = True
        elif hasattr(witness, 'is_noetherian'):
            h1 = bool(witness.is_noetherian)
        elif hasattr(witness, 'is_Noetherian'):
            h1 = bool(witness.is_Noetherian)
        elif witness in [sympy.ZZ, sympy.QQ]:
            h1 = True
    except Exception:
        h1 = False

    # Check ¬Q: The polynomial ring over R is NOT a Noetherian ring
    try:
        if isinstance(witness, str):
            s = witness.lower().strip()
            if s in ["2z", "2zz", "even integers", "ring of even integers"]:
                neg_q = True
            elif "zero mult" in s or "zero-mult" in s:
                neg_q = True
            elif "without identity" in s or "non-unital" in s or "nonunital" in s:
                neg_q = True
            elif s in ["z", "zz", "integers", "q", "qq", "rationals"]:
                neg_q = False
        elif hasattr(witness, 'is_polynomial_ring_noetherian'):
            neg_q = not bool(witness.is_polynomial_ring_noetherian)
        elif hasattr(witness, 'is_poly_noetherian'):
            neg_q = not bool(witness.is_poly_noetherian)
        elif witness in [sympy.ZZ, sympy.QQ]:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The polynomial ring over R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1