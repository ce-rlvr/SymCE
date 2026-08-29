import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_integer(val):
    try:
        if isinstance(val, bool):
            return False
        return int(val) == val
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            a = witness.get('a')
            m_list = list(witness.get('m'))
            if 'M' in witness:
                M = witness['M']
            else:
                M = math.prod(m_list)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                x, a, m_iter = witness
                m_list = list(m_iter)
                M = math.prod(m_list)
            elif len(witness) == 4:
                x, a, m_iter, M = witness
                m_list = list(m_iter)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: M = m_1 m_2 \cdots m_k
    try:
        h1 = False
        if len(m_list) > 0:
            prod = 1
            for m in m_list:
                prod *= int(m)
            h1 = (int(M) == prod)
    except Exception:
        h1 = False

    # H2: x and a are integers
    try:
        h2 = False
        if is_integer(x) and is_integer(a):
            if all(is_integer(m) for m in m_list):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: x \equiv a \pmod{m_i} for all i iff x \equiv a \pmod{M} (Negated)
    try:
        x_val = int(x)
        a_val = int(a)
        M_val = int(M)
        left_side = all((x_val - a_val) % int(m) == 0 for m in m_list)
        right_side = ((x_val - a_val) % M_val == 0)
        neg_q = (left_side != right_side)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M = m_1 m_2 ... m_k",
    "H_2: x and a are integers",
    "¬Q: The equivalence (x ≡ a mod m_i for all i iff x ≡ a mod M) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2