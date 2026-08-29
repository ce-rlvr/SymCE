import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.polys.domains import ZZ, QQ, RR, CC
import sympy.abc

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

def conditions(witness):
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (R, a, b) where R is a domain, 
    and a, b are elements that supposedly have an LCM in R.
    """
    try:
        R, a, b = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    # ¬Q: a and b do NOT have a least common multiple in R
    # In a UFD, any two elements IN the ring have an LCM. 
    # The conclusion fails if a and b are not elements of R, 
    # which makes the existence of an LCM in R undefined or impossible.
    try:
        if a not in R or b not in R:
            has_lcm = False
        else:
            m = R.lcm(a, b)
            has_lcm = (m in R)
    except Exception:
        has_lcm = False
        
    neg_q = not has_lcm
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: a and b do not have a least common multiple in R"
]

N_HYP = 1
NEG_Q_INDEX = 1