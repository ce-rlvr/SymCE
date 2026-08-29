import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The witness can be either (x, y, z) or (G, x, y, z)
        if len(witness) == 3:
            x, y, z = witness
        elif len(witness) == 4:
            _, x, y, z = witness
        else:
            return [False, False]
        
        # H_1: x, y, z are elements of G
        try:
            # Verify that the elements support group operations (multiplication and inversion)
            _ = x * y * z
            _ = x**-1
            _ = y**-1
            _ = z**-1
            h1 = True
        except Exception:
            h1 = False

        # ¬Q: The commutator identity comm(x, yz) = comm(x, z) z^{-1}comm(x, y)z FAILS
        try:
            # In the context where this conjecture is false, the commutator is defined as comm(a, b) = a * b * a^-1 * b^-1
            # (Under the alternative definition comm(a, b) = a^-1 * b^-1 * a * b, the identity would be universally true)
            def comm(a, b):
                return a * b * a**-1 * b**-1
            
            lhs = comm(x, y * z)
            rhs = comm(x, z) * z**-1 * comm(x, y) * z
            
            if hasattr(lhs, 'equals'):
                neg_q = not lhs.equals(rhs)
            else:
                neg_q = (lhs != rhs)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: x, y, z are elements of G", "not Q: comm(x, yz) != comm(x, z) z^-1 comm(x, y) z"]

N_HYP = 1
NEG_Q_INDEX = 1