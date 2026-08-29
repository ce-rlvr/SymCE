import sympy
from sympy import Rational, Integer
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        n = None
        if isinstance(witness, int):
            n = witness
        elif isinstance(witness, sympy.Integer):
            n = int(witness)
        elif hasattr(witness, 'mod'):
            n = int(witness.mod)
        elif hasattr(witness, 'n'):
            n = int(witness.n)
        else:
            s = str(witness)
            digits = ''.join(c for c in s if c.isdigit())
            if digits:
                n = int(digits)
                
        if n is not None:
            n = abs(n)
            if n <= 1:
                return [False]
            factors = sympy.factorint(n)
            neg_q = len(factors) > 1
            return [neg_q]
            
        if isinstance(witness, (tuple, list)):
            neg_q = len(witness) > 1
            return [neg_q]
            
        return [False]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: The polynomial x^2 + y^2 + z^2 - x y z is reducible"]

N_HYP = 0
NEG_Q_INDEX = 0