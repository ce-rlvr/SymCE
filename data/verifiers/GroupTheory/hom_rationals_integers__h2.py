import sympy
from sympy import Rational
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness is expected to be a callable function f: Q -> Z.
    """
    try:
        f = witness
        if not callable(f):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Generate a sample of rational numbers to test the properties
    test_rationals = []
    for p in range(-10, 11):
        for q in range(1, 11):
            test_rationals.append(Rational(p, q))
    test_rationals = list(set(test_rationals))

    # H_1: f maps Q to Z
    try:
        h1 = True
        for r in test_rationals:
            val = f(r)
            if not isinstance(val, (int, sympy.Integer)):
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: f is a group homomorphism (f(a + b) == f(a) + f(b))
    try:
        h2 = True
        for a in test_rationals:
            for b in test_rationals:
                if f(a + b) != f(a) + f(b):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: f is not the trivial homomorphism (there exists r in Q such that f(r) != 0)
    try:
        neg_q = False
        for r in test_rationals:
            if f(r) != 0:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f maps Q to Z",
    "H_2: f is a group homomorphism",
    "¬Q: f is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2