import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def is_inf(n):
    if n == sympy.oo:
        return True
    if isinstance(n, float) and math.isinf(n):
        return True
    if str(n).lower() in ['oo', 'infinity', 'inf', '+inf']:
        return True
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The theorem "Formal Power Series over a Field is a UFD" is true for finitely many variables.
    The dropped hypothesis is that the number of variables n is finite.
    A valid counterexample must specify an infinite number of variables.
    Witness can be a tuple (F, n) or just n (in which case F defaults to QQ).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
        else:
            if is_inf(witness):
                F = sympy.QQ
                n = witness
            else:
                F = witness
                n = 1
                
        try:
            h1 = bool(F.is_Field)
        except Exception:
            h1 = False
            
        try:
            # The formal power series ring F[[x_1 ... x_n]] is a UFD iff n is finite.
            # Thus, the conclusion fails (neg_Q is True) iff n is infinite.
            neg_q = is_inf(n)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: The formal power series ring over F in infinitely many variables is not a UFD"]

N_HYP = 1
NEG_Q_INDEX = 1