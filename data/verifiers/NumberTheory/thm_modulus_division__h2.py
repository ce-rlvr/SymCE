import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: a, b, c, and m are integers",
    "H_2: ac \\equiv bc \\pmod m",
    "H_3: d = \\gcd(c, m)",
    "¬Q: a \\not\\equiv b \\pmod{m/d}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_int(x):
    try:
        return int(x) == x and isinstance(int(x), int)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    a, b, c, m, d = None, None, None, None, None
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            m = witness.get('m')
            if 'd' in witness:
                d = witness['d']
            else:
                if is_int(c) and is_int(m):
                    d = math.gcd(int(c), int(m))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                a, b, c, m = witness
                if is_int(c) and is_int(m):
                    d = math.gcd(int(c), int(m))
            elif len(witness) == 5:
                a, b, c, m, d = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: a, b, c, and m are integers
    try:
        h1 = is_int(a) and is_int(b) and is_int(c) and is_int(m)
    except Exception:
        h1 = False

    # H_2: ac \equiv bc \pmod m
    try:
        if not (is_int(a) and is_int(b) and is_int(c) and is_int(m)):
            h2 = False
        else:
            a_i, b_i, c_i, m_i = int(a), int(b), int(c), int(m)
            if m_i == 0:
                h2 = (a_i * c_i == b_i * c_i)
            else:
                h2 = ((a_i * c_i - b_i * c_i) % m_i == 0)
    except Exception:
        h2 = False

    # H_3: d = \gcd(c, m)
    try:
        if not (is_int(c) and is_int(m) and is_int(d)):
            h3 = False
        else:
            h3 = (int(d) == math.gcd(int(c), int(m)))
    except Exception:
        h3 = False

    # ¬Q: a \not\equiv b \pmod{m/d}
    try:
        if not (is_int(a) and is_int(b) and is_int(m) and is_int(d)):
            q_ok = False
        else:
            a_i, b_i, m_i, d_i = int(a), int(b), int(m), int(d)
            if d_i == 0:
                q_ok = False
            else:
                modulus = m_i // d_i
                if modulus == 0:
                    q_ok = (a_i == b_i)
                else:
                    q_ok = ((a_i - b_i) % modulus == 0)
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]