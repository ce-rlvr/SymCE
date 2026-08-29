import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

class InfiniteBooleanRing:
    """
    Witness for the false conjecture about finitely generated ideals.
    R = Boolean ring of finite subsets of an infinite set.
    This is a commutative ring without identity.
    Let I = R and J = R.
    Then IJ = R^2 = R.
    However, I = R is not finitely generated.
    """
    is_commutative_ring = True
    is_ideal_J = True
    IJ_equals_R = True
    is_I_finitely_generated = False

class InfiniteDirectSumRing:
    """
    Witness for the false conjecture about finitely generated ideals.
    R = Direct sum of infinitely many copies of a field.
    This is a commutative ring without identity.
    Let I = R and J = R.
    Then IJ = R^2 = R.
    However, I = R is not finitely generated.
    """
    is_commutative_ring = True
    is_ideal_J = True
    IJ_equals_R = True
    is_I_finitely_generated = False

def conditions(witness) -> list[bool]:
    try:
        # 1. Check if witness is one of our provided classes or instances
        if hasattr(witness, 'is_commutative_ring') and hasattr(witness, 'is_ideal_J'):
            h1 = bool(witness.is_commutative_ring)
            h2 = bool(witness.is_ideal_J)
            h3 = bool(getattr(witness, 'IJ_equals_R', False) or getattr(witness, 'product_IJ_equals_R', False))
            neg_q = not bool(getattr(witness, 'is_I_finitely_generated', True))
            return [h1, h2, h3, neg_q]
            
        # 2. Check if witness is a dictionary
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring', False))
            h2 = bool(witness.get('is_ideal_J', False))
            h3 = bool(witness.get('IJ_equals_R', False) or witness.get('product_IJ_equals_R', False))
            neg_q = not bool(witness.get('is_I_finitely_generated', True))
            return [h1, h2, h3, neg_q]
            
        # 3. Check if witness is a tuple (R, I, J)
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            R, I, J = witness
            h1 = bool(getattr(R, 'is_commutative_ring', False) or getattr(R, 'is_commutative', False))
            
            if hasattr(J, 'is_ideal_of'):
                h2 = bool(J.is_ideal_of(R))
            else:
                h2 = bool(getattr(J, 'is_ideal', False))
                
            if hasattr(witness, 'IJ_equals_R'):
                h3 = bool(witness.IJ_equals_R)
            else:
                try:
                    h3 = bool(I * J == R)
                except Exception:
                    h3 = False
                    
            neg_q = not bool(getattr(I, 'is_finitely_generated', True))
            
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: The product ideal IJ is equal to the ring R",
    "¬Q: The ideal I is not finitely generated"
]

N_HYP = 3
NEG_Q_INDEX = 3