import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.ntheory import isprime
import math
import itertools
import functools

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
        if isinstance(witness, int):
            n = 2
            m = witness
        elif isinstance(witness, dict):
            n = witness.get('n', 2)
            m = witness.get('m', witness.get('R', None))
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, m = witness
        else:
            n, m = witness, None
    except Exception:
        n, m = 0, None

    try:
        n_val = int(n)
        h1 = n_val >= 2
    except Exception:
        h1 = False

    h2 = True
    h3 = True

    try:
        if m is not None:
            if isinstance(m, int):
                modulus = m
            elif hasattr(m, 'mod'):
                modulus = int(m.mod)
            elif hasattr(m, 'p'):
                modulus = int(m.p)
            elif isinstance(m, str):
                digits = ''.join(c if c.isdigit() else ' ' for c in m).split()
                if digits:
                    modulus = int(digits[-1])
                else:
                    modulus = 0
            else:
                modulus = int(m)
            
            neg_q = modulus > 1 and not isprime(modulus)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: n is an integer such that n >= 2", "H_2: X_ij are algebraically independent variables", "H_3: M is the n x n matrix with entries X_ij", "¬Q: The determinant polynomial det(M) is reducible in R"]

N_HYP = 3
NEG_Q_INDEX = 3