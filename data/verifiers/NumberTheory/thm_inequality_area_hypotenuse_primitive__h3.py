import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
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
    # Extract variables a, b, c, A from the witness.
    # Since the hypothesis defining A as the area was dropped, A is an unconstrained free variable.
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            A = witness['A']
        elif hasattr(witness, 'a'):
            a = witness.a
            b = witness.b
            c = witness.c
            A = witness.A
        else:
            a, b, c, A = witness
    except Exception:
        return [False, False, False]

    # H_1: (a, b, c) is a primitive Pythagorean triple
    try:
        # A primitive Pythagorean triple consists of positive integers
        if int(a) == a and int(b) == b and int(c) == c and a > 0 and b > 0 and c > 0:
            a_i, b_i, c_i = int(a), int(b), int(c)
            is_pyth = (a_i**2 + b_i**2 == c_i**2) or (a_i**2 + c_i**2 == b_i**2) or (b_i**2 + c_i**2 == a_i**2)
            is_prim = math.gcd(a_i, math.gcd(b_i, c_i)) == 1
            h1_ok = bool(is_pyth and is_prim)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: c is the hypotenuse of the triple
    try:
        h2_ok = bool(a**2 + b**2 == c**2)
    except Exception:
        h2_ok = False

    # Negated Conclusion: A is equal to c
    try:
        neg_q_ok = bool(A == c)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple",
    "H_2: c is the hypotenuse of the triple",
    "¬Q: A is equal to c"
]

N_HYP = 2
NEG_Q_INDEX = 2