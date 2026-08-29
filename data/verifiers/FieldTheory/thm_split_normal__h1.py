import sympy
from sympy import Poly, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Rational, Integer

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

x = Symbol('x')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_finite_extension", False))
            is_normal = bool(witness.get("is_normal", False))
            is_splitting = bool(witness.get("is_splitting_field", False))
            neg_q = (is_normal != is_splitting)
        else:
            h1 = bool(getattr(witness, "is_finite_extension", False))
            is_normal = bool(getattr(witness, "is_normal", False))
            is_splitting = bool(getattr(witness, "is_splitting_field", False))
            neg_q = (is_normal != is_splitting)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: K is a finite extension field of F", "¬Q: K is normal iff K is a splitting field (fails)"]
N_HYP = 1
NEG_Q_INDEX = 1