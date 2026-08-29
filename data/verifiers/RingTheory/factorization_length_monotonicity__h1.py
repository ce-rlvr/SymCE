import sympy
from sympy.ntheory import factorint
from sympy.polys import factor_list
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the Factorization Length Monotonicity conjecture.
    Witness is expected to be a tuple (a, b).
    """
    try:
        a, b = witness
    except Exception:
        return [False, False, False]

    def is_unit(x):
        if hasattr(x, 'is_unit'):
            return x.is_unit()
        if isinstance(x, (int, sympy.Integer)):
            return abs(x) == 1
        if hasattr(x, 'is_constant'):
            return x.is_constant()
        return False

    def divides(x, y):
        if hasattr(x, 'divides'):
            return x.divides(y)
        if isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)):
            return y % x == 0
        try:
            _, r = sympy.div(y, x)
            return r == 0
        except Exception:
            return False

    def L(x):
        if hasattr(x, 'prime_factors_count'):
            return x.prime_factors_count()
        if isinstance(x, (int, sympy.Integer)):
            return sum(factorint(abs(int(x))).values())
        return sum(dict(factor_list(x)[1]).values())

    # H_1: a and b are non-zero, non-unit elements of R
    try:
        h1_ok = (a != 0) and (b != 0) and not is_unit(a) and not is_unit(b)
    except Exception:
        h1_ok = False

    # H_2: The principal ideal (a) is strictly contained in the principal ideal (b)
    try:
        h2_ok = divides(b, a) and not divides(a, b)
    except Exception:
        h2_ok = False

    # ¬Q: L(a) <= L(b) (Conclusion L(a) > L(b) fails)
    try:
        neg_q_ok = L(a) <= L(b)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero, non-unit elements",
    "H_2: The principal ideal (a) is strictly contained in the principal ideal (b)",
    "¬Q: L(a) <= L(b)"
]

N_HYP = 2
NEG_Q_INDEX = 2