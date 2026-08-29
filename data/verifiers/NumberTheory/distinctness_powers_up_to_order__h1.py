import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      - a is an integer coprime to n
      - The multiplicative order of a modulo n is d
    Conclusion:
      - The integers 1, a, a^2, ..., a^{d-1} are pairwise incongruent modulo n
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
            d = witness.get('d')
        else:
            a, n, d = witness
    except Exception:
        return [False, False, False]

    # H_1: a is an integer coprime to n
    try:
        h1 = (isinstance(a, int) and isinstance(n, int) and math.gcd(a, n) == 1)
    except Exception:
        h1 = False

    # H_2: The multiplicative order of a modulo n is d
    try:
        if not h1:
            h2 = False
        elif n == 0:
            if a == 1:
                actual_d = 1
            elif a == -1:
                actual_d = 2
            else:
                actual_d = None
            h2 = (actual_d is not None and d == actual_d)
        elif abs(n) == 1:
            h2 = (d == 1)
        else:
            actual_d = sympy.n_order(a, abs(n))
            h2 = (d == actual_d)
    except Exception:
        h2 = False

    # ¬Q: The integers 1, a, a^2, ..., a^{d-1} are NOT pairwise incongruent modulo n
    # This means there are duplicates when evaluated modulo n.
    try:
        if not (isinstance(d, int) and d >= 0):
            neg_q = False
        elif n == 0:
            s = set()
            for i in range(d):
                s.add(a**i)
            neg_q = len(s) < d
        else:
            s = set()
            val = 1
            abs_n = abs(n)
            for i in range(d):
                s.add(val)
                val = (val * a) % abs_n
            neg_q = len(s) < d
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to n",
    "H_2: The multiplicative order of a modulo n is d",
    "¬Q: The integers 1, a, a^2, ..., a^{d-1} are not pairwise incongruent modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2