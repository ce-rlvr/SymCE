import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: H is the subgroup mZ",
    "H_3: K is the subgroup nZ",
    "¬Q: The intersection H \\cap K is not the subgroup lcm(m, n)Z"
]

N_HYP = 3
NEG_Q_INDEX = 3

class Multiples:
    def __init__(self, base):
        self.base = int(base) if isinstance(base, (int, sympy.Integer)) else base
        
    def __contains__(self, item):
        if not isinstance(self.base, int):
            return False
        if self.base == 0:
            return item == 0
        return item % self.base == 0

def in_set(S, i):
    if isinstance(S, (int, sympy.Integer)):
        S_val = int(S)
        return (i % S_val == 0) if S_val != 0 else (i == 0)
    if hasattr(S, '__contains__'):
        try:
            return bool(i in S)
        except Exception:
            pass
    try:
        return bool(S.contains(sympy.sympify(i)))
    except Exception:
        return False

def is_mZ(S, m):
    if not isinstance(m, (int, sympy.Integer)):
        return False
    m_val = int(m)
    for i in range(-100, 101):
        expected = (i % m_val == 0) if m_val != 0 else (i == 0)
        if in_set(S, i) != expected:
            return False
    return True

def check_conclusion(H, K, m, n):
    m_val = int(m)
    n_val = int(n)
    try:
        l = math.lcm(m_val, n_val)
    except AttributeError:
        l = int(sympy.lcm(m_val, n_val))
        
    for i in range(-100, 101):
        in_intersection = in_set(H, i) and in_set(K, i)
        expected = (i % l == 0) if l != 0 else (i == 0)
        if in_intersection != expected:
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            H = witness.get('H', Multiples(m) if m is not None else None)
            K = witness.get('K', Multiples(n) if n is not None else None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                m, n = witness
                H, K = Multiples(m), Multiples(n)
            elif len(witness) >= 4:
                m, n, H, K = witness[:4]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: m and n are positive integers
    try:
        h1_ok = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1_ok = False

    # H_2: H is the subgroup mZ
    try:
        h2_ok = is_mZ(H, m)
    except Exception:
        h2_ok = False

    # H_3: K is the subgroup nZ
    try:
        h3_ok = is_mZ(K, n)
    except Exception:
        h3_ok = False

    # ¬Q: The intersection H \cap K is not the subgroup lcm(m, n)Z
    try:
        neg_q = not check_conclusion(H, K, m, n)
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q)]