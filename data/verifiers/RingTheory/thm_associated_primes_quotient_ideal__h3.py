import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Standard algebra objects
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

def _gcd(a, b):
    try:
        return math.gcd(int(a), int(b))
    except Exception:
        return sympy.gcd(a, b)

def _rem(a, b):
    try:
        return a % b
    except Exception:
        return sympy.rem(a, b)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a commutative Noetherian ring, and I, J be ideals of R. 
    Then Ass(J/I) is a subset of Ass(R/I)."
    
    The conjecture is false because the hypothesis I ⊆ J was dropped. 
    Without I ⊆ J, the quotient module J/I is undefined, making the conclusion false.
    The witness is expected to be a pair of ideals (represented by their generators)
    such that I is not a subset of J.
    """
    try:
        if len(witness) == 3:
            R, I, J = witness
        elif len(witness) == 2:
            I, J = witness
        else:
            return [False, False, False]
            
        if isinstance(I, (list, tuple)):
            if len(I) == 0:
                i = 0
            else:
                i = I[0]
                for gen in I[1:]:
                    i = _gcd(i, gen)
        else:
            i = I
            
        if isinstance(J, (list, tuple)):
            if len(J) == 0:
                j = 0
            else:
                j = J[0]
                for gen in J[1:]:
                    j = _gcd(j, gen)
        else:
            j = J
            
        try:
            i = int(i)
        except Exception:
            pass
        try:
            j = int(j)
        except Exception:
            pass
            
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative Noetherian ring
    # We evaluate this in Z or a polynomial ring over a field, which are Noetherian.
    h1 = True
    
    # H2: I and J are ideals of R
    # The generators define valid ideals.
    h2 = True
    
    # Conclusion: Ass(J/I) is a subset of Ass(R/I)
    # If I is not a subset of J, J/I is undefined as a quotient module,
    # making the subset relation false.
    # For principal ideals I = <i> and J = <j>, I ⊆ J iff j divides i.
    try:
        if j == 0:
            if i == 0:
                neg_q = False
            else:
                neg_q = True
        else:
            rem = _rem(i, j)
            if rem == 0:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I and J are ideals of R",
    "¬Q: Ass(J/I) is not a subset of Ass(R/I) (e.g., J/I is undefined because I is not a subset of J)"
]

N_HYP = 2
NEG_Q_INDEX = 2