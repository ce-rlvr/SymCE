import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    h1 = True
    h2 = True
    h3 = True
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if 'h1' in witness: h1 = bool(witness['h1'])
            if 'h2' in witness: h2 = bool(witness['h2'])
            if 'h3' in witness: h3 = bool(witness['h3'])
            if 'is_unit' in witness and 'is_automorphism' in witness:
                neg_q = bool(witness['is_unit']) != bool(witness['is_automorphism'])
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_unit') and hasattr(witness, 'is_automorphism'):
            u = witness.is_unit
            a = witness.is_automorphism
            if callable(u): u = u()
            if callable(a): a = a()
            neg_q = bool(u) != bool(a)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'f'):
            f = witness.f
            if hasattr(f, 'is_unit') and hasattr(f, 'is_automorphism'):
                u = f.is_unit
                a = f.is_automorphism
                if callable(u): u = u()
                if callable(a): a = a()
                neg_q = bool(u) != bool(a)
                return [h1, h2, h3, neg_q]
            if isinstance(f, Matrix):
                neg_q = False
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, M, f = witness
            if isinstance(f, Matrix):
                neg_q = False
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, Matrix):
            neg_q = False
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is a left R-module",
    "H_3: End_R(M) is the ring of R-module endomorphisms of M under point-wise addition and function composition",
    "¬Q: f is a unit in End_R(M) XOR f is an R-module automorphism of M"
]

N_HYP = 3
NEG_Q_INDEX = 3