import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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

def conditions(witness):
    """
    Checks the witness against the hypotheses and negated conclusion.
    The witness is expected to be a tuple: (R, K, x)
    where R is a SymPy domain (e.g., ZZ), K is a SymPy field (e.g., QQ.algebraic_field(sqrt(2))),
    and x is an element.
    """
    try:
        R, K, x = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: x is a non-zero element of K
    try:
        if hasattr(K, 'is_Field') and K.is_Field:
            x_K = K.convert(x)
            h2 = bool(x_K != K.zero)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: There do not exist coprime elements a, b \in R such that x = a/b
    try:
        F = R.frac_field()
        x_F = F.convert(x)
        num = F.numer(x_F)
        den = F.denom(x_F)
        gcd = R.gcd(num, den)
        num_red = R.exquo(num, gcd)
        den_red = R.exquo(den, gcd)
        
        if R.is_unit(R.gcd(num_red, den_red)):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        # If x cannot be converted to the fraction field of R, or operations fail,
        # it cannot be represented as a/b for a, b in R.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: x is a non-zero element of K",
    "¬Q: There do not exist coprime elements a, b in R such that x = a/b"
]

N_HYP = 2
NEG_Q_INDEX = 2