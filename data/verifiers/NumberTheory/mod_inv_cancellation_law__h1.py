import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            m = witness.get('m')
        else:
            a, b, c, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: m is a positive integer
    try:
        m_sym = sympy.sympify(m)
        h1 = bool(m_sym.is_integer and m_sym > 0)
    except Exception:
        h1 = False

    # H2: gcd(c, m) = 1
    try:
        c_sym = sympy.sympify(c)
        m_sym = sympy.sympify(m)
        h2 = bool(sympy.gcd(c_sym, m_sym) == 1)
    except Exception:
        h2 = False

    # H3: a * c ≡ b * c (mod m)
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        c_sym = sympy.sympify(c)
        m_sym = sympy.sympify(m)
        diff = a_sym * c_sym - b_sym * c_sym
        h3 = bool((diff % m_sym) == 0)
    except Exception:
        h3 = False

    # neg_Q: a ≢ b (mod m)
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        m_sym = sympy.sympify(m)
        diff_ab = a_sym - b_sym
        neg_q = not bool((diff_ab % m_sym) == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: gcd(c, m) = 1",
    "H_3: a * c \u2261 b * c (mod m)",
    "\u00acQ: a \u2262 b (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3