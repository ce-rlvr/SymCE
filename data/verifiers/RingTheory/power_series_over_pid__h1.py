import sympy
from sympy import Symbol, eye, zeros, Rational, Integer

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        is_f = False
        if getattr(witness, 'is_Field', False):
            is_f = True
        elif hasattr(witness, 'is_field'):
            val = witness.is_field() if callable(witness.is_field) else witness.is_field
            if val:
                is_f = True
        else:
            name = str(witness).lower()
            if name in ['q', 'r', 'c', 'qq', 'rr', 'cc', 'field']:
                is_f = True
        h1_ok = not is_f
    except Exception:
        h1_ok = False

    try:
        is_div = is_f
        if not is_div:
            name = str(witness).lower()
            if any(kw in name for kw in ['quaternion', 'division', 'skew']):
                is_div = True
            elif hasattr(witness, 'is_commutative') and witness.is_commutative is False:
                if 'matrix' not in name:
                    is_div = True
        neg_q_ok = is_div
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "not Q: The formal power series ring over R is a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1