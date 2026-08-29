import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The ideal quotient (I : xy) is not equal to the iterated ideal quotient ((I : x) : y)"
]

def conditions(witness):
    # Unpack witness
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            x = witness.get('x')
            y = witness.get('y')
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            x = witness.x
            y = witness.y
        else:
            R, I, x, y = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring(R))
        elif R == sympy.ZZ or R == sympy.QQ:
            h1 = True
    except Exception:
        pass

    # H2: I is an ideal of R
    h2 = False
    try:
        if hasattr(I, 'ring'):
            h2 = bool(I.ring == R)
        elif hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal(R))
        elif hasattr(witness, 'is_ideal'):
            h2 = bool(witness.is_ideal(I, R))
        elif isinstance(I, int) and R == sympy.ZZ:
            h2 = True
        else:
            h2 = hasattr(I, 'contains') and hasattr(I, 'subset')
    except Exception:
        pass

    # neg_Q: (I : xy) != ((I : x) : y)
    neg_q = False
    try:
        I_xy = I.quotient(x * y)
        I_x = I.quotient(x)
        I_x_y = I_x.quotient(y)
        neg_q = bool(I_xy != I_x_y)
    except Exception:
        try:
            # Try treating x and y as elements generating principal ideals
            I_xy = I.quotient(R.ideal(x * y))
            I_x = I.quotient(R.ideal(x))
            I_x_y = I_x.quotient(R.ideal(y))
            neg_q = bool(I_xy != I_x_y)
        except Exception:
            try:
                # Try custom quotient method on witness
                I_xy = witness.quotient(I, x * y)
                I_x = witness.quotient(I, x)
                I_x_y = witness.quotient(I_x, y)
                neg_q = bool(I_xy != I_x_y)
            except Exception:
                try:
                    # Try integer ideal quotient fallback
                    if isinstance(I, int) and isinstance(x, int) and isinstance(y, int):
                        I_xy = I // math.gcd(I, x * y)
                        I_x = I // math.gcd(I, x)
                        I_x_y = I_x // math.gcd(I_x, y)
                        neg_q = bool(I_xy != I_x_y)
                except Exception:
                    pass

    return [h1, h2, neg_q]