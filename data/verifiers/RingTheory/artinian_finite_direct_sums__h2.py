import sympy
import sympy.abc
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.abc.x

def is_ring(R):
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring:
            return True
        if R.__class__.__name__ in ('IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'PolynomialRing', 'AlgebraicField', 'FiniteField'):
            return True
        if R in (sympy.ZZ, sympy.QQ):
            return True
    except Exception:
        pass
    return False

def is_artinian_ring(R):
    try:
        if getattr(R, 'is_Field', False) or R.__class__.__name__ in ('RationalField', 'RealField', 'ComplexField', 'AlgebraicField', 'FiniteField'):
            return True
        if R == sympy.ZZ:
            return False
        if R.__class__.__name__ == 'PolynomialRing':
            return False
        if hasattr(R, 'domain') and R.domain == sympy.ZZ:
            return False
    except Exception:
        pass
    return False

def is_artinian_module(R, M):
    try:
        if isinstance(M, int):
            if M == 0:
                return True
            return is_artinian_ring(R)
        if M == R:
            return is_artinian_ring(R)
        if getattr(M, 'is_Field', False) or M.__class__.__name__ in ('RationalField', 'RealField', 'ComplexField', 'AlgebraicField', 'FiniteField'):
            if R == sympy.ZZ and M == sympy.QQ:
                return False
            if R == M:
                return True
        if M.__class__.__name__ == 'PolynomialRing':
            return False
        if hasattr(M, 'order') and M.order() < float('inf'):
            return True
    except Exception:
        pass
    return is_artinian_ring(R)

def conditions(witness) -> list[bool]:
    try:
        # The witness can be either a tuple (R, [M_1, M_2, ..., M_n]) or just a ring R.
        # If just a ring R is provided, we assume the modules are R itself.
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            R, M_list = witness
        else:
            R = witness
            M_list = [R, R]
    except Exception:
        return [False, False]

    try:
        h1_ok = is_ring(R)
    except Exception:
        h1_ok = False

    try:
        # The conclusion is that the direct sum of M_1, ..., M_n is an Artinian R-module.
        # A finite direct sum is Artinian iff every summand is Artinian.
        # Therefore, the conclusion fails (neg_Q is True) iff at least one M_i is NOT Artinian.
        all_artinian = all(is_artinian_module(R, M) for M in M_list)
        neg_q_ok = not all_artinian
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: The direct sum of M_1, M_2, ..., M_n is not an Artinian R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1