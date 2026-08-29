import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness should provide the ring R, and elements a, b, d.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', sympy.ZZ)
            a = witness['a']
            b = witness['b']
            d = witness['d']
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, a, b, d = witness
            elif len(witness) == 3:
                a, b, d = witness
                R = sympy.ZZ
            else:
                return [False, False, False]
        else:
            R = witness.R
            a = witness.a
            b = witness.b
            d = witness.d
    except Exception:
        return [False, False, False]

    def divides(x_val, y_val):
        if x_val == 0:
            return y_val == 0
        try:
            if hasattr(R, 'rem'):
                return R.rem(y_val, x_val) == 0
        except Exception:
            pass
        try:
            return y_val % x_val == 0
        except Exception:
            pass
        return False

    # H_1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # H_2: d is a greatest common divisor of a and b
    try:
        div_a = divides(d, a)
        div_b = divides(d, b)
        if not (div_a and div_b):
            h2 = False
        else:
            if hasattr(R, 'gcd'):
                actual_gcd = R.gcd(a, b)
                # In a PID, any common divisor must divide the greatest common divisor
                h2 = divides(actual_gcd, d)
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The tensor product R/<a> ⊗_R R/<b> is NOT isomorphic to R/<d> as R-modules
    try:
        is_comm = getattr(R, 'is_commutative', True)
        if is_comm:
            # For a commutative PID, R/<a> ⊗_R R/<b> is isomorphic to R/<gcd(a,b)>.
            # It is isomorphic to R/<d> if and only if d and gcd(a,b) are associate.
            if hasattr(R, 'gcd'):
                actual_gcd = R.gcd(a, b)
                isomorphic = divides(d, actual_gcd) and divides(actual_gcd, d)
                neg_q = not isomorphic
            else:
                neg_q = False
        else:
            # For non-commutative PIDs, the tensor product of R/<a> and R/<b> over R
            # is generally undefined (unless <a> is a two-sided ideal) or not isomorphic to R/<d>.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: The tensor product R/<a> ⊗_R R/<b> is not isomorphic to R/<d> as R-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2