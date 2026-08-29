import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: x_1 is an integer such that a x_1 ≡ b (mod m)",
    "H_3: x_2 is an integer such that a x_2 ≡ b (mod m)",
    "¬Q: x_1 is not congruent to x_2 mod (m / gcd(a, m))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_int(x):
    if isinstance(x, int):
        return True
    if isinstance(x, sympy.Integer):
        return True
    if hasattr(x, 'is_integer'):
        if callable(x.is_integer):
            return x.is_integer()
        else:
            return bool(x.is_integer)
    return False

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness.get('a'), witness.get('b'), witness.get('m'), witness.get('x_1'), witness.get('x_2')
    elif isinstance(witness, (list, tuple)):
        if len(witness) >= 5:
            return witness[0], witness[1], witness[2], witness[3], witness[4]
    raise ValueError("Invalid witness format")

def conditions(witness):
    try:
        a, b, m, x_1, x_2 = parse_witness(witness)
    except Exception:
        return [False, False, False, False]

    # H_1: a and b are integers
    try:
        h1 = is_int(a) and is_int(b)
    except Exception:
        h1 = False

    # H_2: x_1 is an integer such that a x_1 ≡ b (mod m)
    try:
        h2 = False
        if is_int(x_1):
            if m == 0:
                h2 = (a * x_1 == b)
            else:
                h2 = ((a * x_1 - b) % m == 0)
    except Exception:
        h2 = False

    # H_3: x_2 is an integer such that a x_2 ≡ b (mod m)
    try:
        h3 = False
        if is_int(x_2):
            if m == 0:
                h3 = (a * x_2 == b)
            else:
                h3 = ((a * x_2 - b) % m == 0)
    except Exception:
        h3 = False

    # ¬Q: x_1 ≢ x_2 (mod m / gcd(a, m))
    try:
        if not (is_int(a) and is_int(m)):
            neg_q = (x_1 != x_2)
        else:
            a_int = int(a)
            m_int = int(m)
            if m_int == 0:
                # Modulus is undefined (0/0), so the congruence statement is meaningless/false.
                neg_q = (x_1 != x_2)
            else:
                d = math.gcd(a_int, m_int)
                modulus = abs(m_int) // d
                if modulus == 0:
                    neg_q = (x_1 != x_2)
                else:
                    neg_q = ((x_1 - x_2) % modulus != 0)
    except Exception:
        neg_q = (x_1 != x_2)

    return [h1, h2, h3, neg_q]