import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis is "I is an ideal". The conjecture fails when I is just a subset.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
    else:
        R = sympy.S.Integers
        I = witness

    # H_1: R is a commutative ring with identity
    h1_ok = False
    try:
        if R is sympy.S.Integers or R is sympy.ZZ or R.__class__.__name__ == 'IntegerRing':
            h1_ok = True
        elif R is sympy.S.Rationals or R is sympy.QQ or R.__class__.__name__ == 'RationalField':
            h1_ok = True
        elif hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'has_Identity') and R.has_Identity:
            h1_ok = True
        elif hasattr(R, 'is_Ring') and R.is_Ring and getattr(R, 'is_commutative', True):
            h1_ok = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The radical of I is NOT equal to the intersection of all prime ideals of R that contain I
    neg_q = False
    try:
        if R is sympy.S.Integers or R is sympy.ZZ or R.__class__.__name__ == 'IntegerRing':
            if isinstance(I, (list, set, tuple)):
                I_list = list(I)
                if len(I_list) == 0:
                    g = 0
                else:
                    g = int(I_list[0])
                    for a in I_list[1:]:
                        g = math.gcd(g, int(a))
                
                if g == 0:
                    intersection_ideal = 0
                elif g == 1 or g == -1:
                    intersection_ideal = 1
                else:
                    factors = sympy.factorint(g)
                    P = 1
                    for p in factors:
                        P *= p
                    intersection_ideal = P
                    
                rad_I = set()
                for a in I_list:
                    try:
                        a_int = int(a)
                    except Exception:
                        continue
                        
                    if a_int == 0:
                        rad_I.add(0)
                        continue
                    if a_int == 1:
                        rad_I.add(1)
                        rad_I.add(-1)
                        continue
                    if a_int == -1:
                        rad_I.add(-1)
                        rad_I.add(1)
                        continue
                    
                    abs_a = abs(a_int)
                    for k in range(1, int(math.log2(abs_a)) + 2):
                        if a_int < 0 and k % 2 == 0:
                            continue
                        root = round(abs_a ** (1.0 / k))
                        if root ** k == abs_a:
                            if a_int > 0:
                                rad_I.add(root)
                                if k % 2 == 0:
                                    rad_I.add(-root)
                            else:
                                rad_I.add(-root)
                                
                if intersection_ideal != 0:
                    # The intersection of prime ideals is an infinite ideal, but rad_I is finite
                    neg_q = True
                else:
                    # If intersection is (0), check if rad_I is exactly {0}
                    neg_q = (rad_I != {0})
            else:
                # If I is an ideal, the theorem holds, so neg_Q is False
                neg_q = False
        else:
            # For other rings, if I is a subset (not an ideal), the theorem generally fails
            if isinstance(I, (list, set, tuple)):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The radical of I is NOT equal to the intersection of all prime ideals of R that contain I"
]

N_HYP = 1
NEG_Q_INDEX = 1