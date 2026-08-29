import sympy
from sympy import ZZ, QQ
import math

# Top-level setup
# ZZ and QQ are provided as standard commutative rings.
# Integers n >= 2 can be used to represent the ring Z/nZ.
# Integer 0 can be used to represent the ring Z.

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
            
        if len(witness) == 3:
            R, a, b = witness
        elif len(witness) == 2:
            R = ZZ
            a, b = witness
        else:
            return [False, False, False]
            
        # H_1: R is a commutative ring with identity
        h1 = False
        if R is ZZ or R is QQ:
            h1 = True
        elif isinstance(R, int) and (R == 0 or R >= 2):
            h1 = True
            
        # H_2: a and b are elements of R
        h2 = False
        if R is ZZ or (isinstance(R, int) and R == 0):
            try:
                h2 = (a == int(a)) and (b == int(b))
            except Exception:
                h2 = False
        elif R is QQ:
            try:
                sympy.Rational(a)
                sympy.Rational(b)
                h2 = True
            except Exception:
                h2 = False
        elif isinstance(R, int) and R >= 2:
            try:
                h2 = (a == int(a)) and (b == int(b)) and (0 <= int(a) < R) and (0 <= int(b) < R)
            except Exception:
                h2 = False
                
        # ¬Q: Not both a and b are units in R
        a_is_unit = False
        b_is_unit = False
        
        if R is ZZ or (isinstance(R, int) and R == 0):
            try:
                a_is_unit = (abs(int(a)) == 1)
                b_is_unit = (abs(int(b)) == 1)
            except Exception:
                pass
        elif R is QQ:
            try:
                a_is_unit = (sympy.Rational(a) != 0)
                b_is_unit = (sympy.Rational(b) != 0)
            except Exception:
                pass
        elif isinstance(R, int) and R >= 2:
            try:
                a_is_unit = (math.gcd(int(a), R) == 1)
                b_is_unit = (math.gcd(int(b), R) == 1)
            except Exception:
                pass
            
        neg_q = not (a_is_unit and b_is_unit)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: a and b are elements of R",
    "¬Q: Not both a and b are units in R"
]

N_HYP = 2
NEG_Q_INDEX = 2