import sympy
from sympy import Poly
from sympy.abc import x

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a non-constant polynomial",
    "not Q: the factor ring is semisimple iff f is square-free fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f = witness
        elif hasattr(witness, "free_symbols"):
            free = witness.free_symbols
            if len(free) == 1:
                var = list(free)[0]
                f = Poly(witness, var)
            else:
                f = Poly(witness, x)
        else:
            f = Poly(witness, x)
    except Exception:
        return [False, False]
        
    try:
        if not f.is_univariate or f.is_zero:
            h1 = False
        else:
            h1 = bool(f.degree() >= 1)
    except Exception:
        h1 = False
        
    try:
        is_sqf = f.is_squarefree
        if is_sqf is None:
            neg_q = False
        else:
            domain = f.domain
            if domain.is_Field:
                is_semi = is_sqf
            else:
                is_semi = False
            neg_q = bool(is_semi != is_sqf)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]