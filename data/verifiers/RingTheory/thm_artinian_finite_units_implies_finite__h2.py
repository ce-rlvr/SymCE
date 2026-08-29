import sympy
from sympy import QQ, ZZ, RR, CC, GF
import sympy.combinatorics
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.DihedralGroup(2)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_ring(obj):
    if obj in [QQ, ZZ, RR, CC, sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
        return True
    if hasattr(obj, 'is_Field'):
        return True
    if obj.__class__.__name__ in ['GaloisField', 'PolynomialRing', 'FractionField', 'RationalField', 'RealField', 'ComplexField', 'IntegerRing']:
        return True
    return False

def is_finite(ring):
    if not is_ring(ring):
        return False
    try:
        if ring in [QQ, ZZ, RR, CC, sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            return False
        if ring.__class__.__name__ == 'GaloisField':
            return True
        if hasattr(ring, 'is_FiniteField') and ring.is_FiniteField:
            return True
    except Exception:
        pass
    return False

def is_artinian(ring):
    if not is_ring(ring):
        return False
    try:
        if ring in [QQ, RR, CC, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            return True
        if ring in [ZZ, sympy.S.Integers]:
            return False
        if hasattr(ring, 'is_Field') and ring.is_Field:
            return True
        if ring.__class__.__name__ == 'PolynomialRing':
            return False
        if is_finite(ring):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        h1 = is_artinian(witness)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_finite(witness) and is_ring(witness)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1