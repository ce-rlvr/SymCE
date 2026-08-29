import sympy
from sympy import I, Rational, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import math
import itertools
import functools

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
    "¬Q: The group of units of R is not exactly {1, -1, i, -i}"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    neg_q = False
    expected_units = {1, -1, I, -I}
    
    if isinstance(witness, (set, list, tuple)):
        try:
            neg_q = set(witness) != expected_units
        except Exception:
            neg_q = False
    else:
        try:
            # Check if any expected unit is missing from the ring
            missing_unit = False
            for u in expected_units:
                if u not in witness:
                    missing_unit = True
                    break
            
            if missing_unit:
                # If an expected unit is missing, the units cannot be exactly {1, -1, I, -I}
                neg_q = True
            else:
                # All expected units are present. Check if there are extra units.
                # If 1/2 is in the ring, then 2 is a unit, which is not in the expected set.
                if Rational(1, 2) in witness:
                    neg_q = True
                elif Rational(1, 3) in witness:
                    neg_q = True
                # If (1-I)/2 is in the ring, then 1+I is a unit, which is not in the expected set.
                elif (1 - I) / 2 in witness:
                    neg_q = True
                else:
                    # We cannot definitively prove there are extra units,
                    # so we conservatively return False (not a proven counterexample).
                    neg_q = False
        except Exception:
            neg_q = False
            
    return [neg_q]