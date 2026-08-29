import math
import itertools
import functools
import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple (x_seq, S, epsilon) or a dict with these keys, where:
      - x_seq is a callable representing the sequence x_n
      - S is a list/set of floats representing the subsequential limits
      - epsilon is a float
    """
    try:
        if isinstance(witness, dict):
            x_seq = witness['x']
            S = witness['S']
            epsilon = witness['epsilon']
        else:
            x_seq, S, epsilon = witness
    except Exception:
        return [False, False, False]

    # H1: (x_n) is a bounded sequence of real numbers
    try:
        vals = [float(x_seq(n)) for n in range(1, 10001)]
        h1 = (max(vals) - min(vals)) < 1e6
    except Exception:
        h1 = False

    # H2: S is the set of all subsequential limits of (x_n)
    try:
        S_floats = [float(s) for s in S]
        if not S_floats:
            h2 = False
        else:
            s_approached = True
            for s in S_floats:
                count = sum(1 for n in range(5000, 10001) if abs(float(x_seq(n)) - s) < 5e-2)
                if count < 1:
                    s_approached = False
                    break
            
            no_other_limits = True
            for n in range(9500, 10001):
                if min(abs(float(x_seq(n)) - s) for s in S_floats) > 5e-2:
                    no_other_limits = False
                    break
                    
            h2 = s_approached and no_other_limits
    except Exception:
        h2 = False

    # neg_Q: There are infinitely many indices n such that inf_{s \in S} |x_n - s| >= epsilon
    try:
        eps = float(epsilon)
        count = 0
        S_floats = [float(s) for s in S]
        for n in range(5000, 10001):
            dist = min(abs(float(x_seq(n)) - s) for s in S_floats)
            if dist >= eps - 1e-9:
                count += 1
        # If it happens frequently in the tail, we consider it "infinitely many"
        neg_q = count > 100
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a bounded sequence of real numbers",
    "H_2: S is the set of all subsequential limits of (x_n)",
    "¬Q: There are infinitely many indices n such that inf_{s in S} |x_n - s| >= epsilon"
]

N_HYP = 2
NEG_Q_INDEX = 2