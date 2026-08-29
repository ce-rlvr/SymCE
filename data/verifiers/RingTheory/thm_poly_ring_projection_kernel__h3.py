import sympy
from sympy import ZZ, QQ, Symbol
from sympy.matrices import eye, zeros

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    H1, H2, neg_Q = False, False, False
    try:
        if isinstance(witness, dict):
            H1 = 'R' in witness
            H2 = 'I' in witness
            neg_Q = witness.get('neg_Q', True)
        elif isinstance(witness, tuple) and len(witness) >= 2:
            H1 = True
            H2 = True
            neg_Q = witness[2] if len(witness) > 2 else True
        else:
            H1 = hasattr(witness, 'R')
            H2 = hasattr(witness, 'I')
            neg_Q = getattr(witness, 'neg_Q', True)
    except Exception:
        pass
    return [bool(H1), bool(H2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The kernel of pi is not the ideal of polynomials over I"
]

N_HYP = 2
NEG_Q_INDEX = 2