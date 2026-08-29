import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    """
    Expected witness format:
    A tuple (n, R, I) or a dict/object with these keys/attributes, where:
      n is an integer > 0 (the modulus for Z_n)
      R is a list/set of integers representing a subring of Z_n
      I is a list/set of integers representing an ideal of R
    """
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'R') and hasattr(witness, 'I'):
            n = witness.n
            R_set = witness.R
            I_set = witness.I
        elif isinstance(witness, dict):
            n = witness['n']
            R_set = witness['R']
            I_set = witness['I']
        else:
            n, R_set, I_set = witness
            
        n = int(n)
        if n <= 0:
            return [False, False]
            
        R = set(r % n for r in R_set)
        I = set(i % n for i in I_set)
        
        # H1: R is a commutative ring
        h1 = True
        if not R:
            h1 = False
        else:
            for a in R:
                if (-a) % n not in R:
                    h1 = False
                for b in R:
                    if (a + b) % n not in R:
                        h1 = False
                    if (a * b) % n not in R:
                        h1 = False
                        
        # Check if I is an ideal of R (required for the conclusion to make sense)
        is_ideal = True
        if not I.issubset(R) or not I:
            is_ideal = False
        else:
            for a in I:
                if (-a) % n not in I:
                    is_ideal = False
                for b in I:
                    if (a + b) % n not in I:
                        is_ideal = False
            for r in R:
                for i in I:
                    if (r * i) % n not in I:
                        is_ideal = False
                        
        # neg_Q: Ann(R/I) != I
        if not is_ideal:
            neg_q = False
        else:
            ann = set()
            for r in R:
                annihilates = True
                for x in R:
                    if (r * x) % n not in I:
                        annihilates = False
                        break
                if annihilates:
                    ann.add(r)
            neg_q = (ann != I)
            
    except Exception:
        h1 = False
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The annihilator of R/I is not exactly the ideal I"
]

N_HYP = 1
NEG_Q_INDEX = 1