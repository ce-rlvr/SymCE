import sympy
from sympy import Poly, factor_list, sqrt, Rational
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    h1_ok = False
    try:
        if isinstance(witness, sympy.Expr) and witness.free_symbols.issubset({x}):
            p = Poly(witness, x)
            if 1 <= p.degree() <= 10:
                h1_ok = all(c.is_Rational for c in p.coeffs())
    except Exception:
        h1_ok = False

    neg_q = False
    if h1_ok:
        try:
            ext_K = [sqrt(-3), 2**Rational(1, 3)]
            ext_sub = [sqrt(-3)]
            
            factors_K = factor_list(witness, extension=ext_K)[1]
            splits_in_K = all(Poly(fac, x).degree() == 1 for fac, mult in factors_K)
            
            if not splits_in_K:
                neg_q = True
            else:
                factors_sub = factor_list(witness, extension=ext_sub)[1]
                splits_in_sub = all(Poly(fac, x).degree() == 1 for fac, mult in factors_sub)
                
                if splits_in_sub:
                    neg_q = True
                else:
                    neg_q = False
        except Exception:
            neg_q = False
            
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: witness is a polynomial over Q",
    "¬Q: The splitting field E is not the expected field or its degree is not 6"
]

N_HYP = 1
NEG_Q_INDEX = 1