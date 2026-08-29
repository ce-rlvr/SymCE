import sympy
from sympy import Poly, sympify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: R is a UFD with field of fractions K",
    "¬Q: The conclusion fails for f"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_orig = witness[-1]
        else:
            f_orig = witness
            
        h1 = True
        
        try:
            f = sympify(f_orig)
            if f == 0:
                neg_q = True
            else:
                syms = f.free_symbols
                if not syms:
                    if f.is_number and f.is_real:
                        if f.is_Rational or f.is_Float:
                            neg_q = False
                        else:
                            neg_q = True
                    else:
                        neg_q = True
                else:
                    var = list(syms)[0]
                    p = Poly(f, var)
                    if not all((c.is_Rational or c.is_Float) for c in p.coeffs()):
                        neg_q = True
                    else:
                        neg_q = False
        except Exception:
            neg_q = True
            
        return [h1, neg_q]
    except Exception:
        return [False, False]