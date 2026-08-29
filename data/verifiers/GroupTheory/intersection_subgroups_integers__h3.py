import math
import itertools
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def is_int(x):
    return isinstance(x, (int, sympy.Integer))

def conditions(witness) -> list[bool]:
    """
    witness: tuple (h, m, n, k) of integers.
    Represents the subgroup H = hZ, positive integers m and n, and subgroup K = kZ.
    Alternatively, a dict with keys 'h' (or 'H'), 'm', 'n', 'k' (or 'K').
    """
    try:
        if isinstance(witness, dict):
            h = witness.get('h', witness.get('H'))
            m = witness.get('m')
            n = witness.get('n')
            k = witness.get('k', witness.get('K'))
        else:
            h, m, n, k = witness
    except Exception:
        return [False, False, False]

    # H_1: m and n are positive integers
    try:
        h1 = is_int(m) and is_int(n) and m > 0 and n > 0
    except Exception:
        h1 = False

    # H_2: K is the subgroup nZ
    try:
        h2 = is_int(k) and is_int(n) and abs(k) == abs(n)
    except Exception:
        h2 = False

    # neg_Q: H \cap K is not the subgroup lcm(m, n)Z
    try:
        if not (is_int(h) and is_int(k) and is_int(m) and is_int(n)):
            neg_q = False
        else:
            actual_lcm = math.lcm(abs(int(h)), abs(int(k)))
            claimed_lcm = math.lcm(abs(int(m)), abs(int(n)))
            neg_q = actual_lcm != claimed_lcm
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: K is the subgroup nZ",
    "¬Q: H \\cap K is not the subgroup lcm(m, n)Z"
]

N_HYP = 2
NEG_Q_INDEX = 2