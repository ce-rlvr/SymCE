import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Unpack witness safely
    try:
        if isinstance(witness, dict):
            M = witness.get('M')
            n = witness.get('n')
            P = witness.get('P')
            R = witness.get('R', None)
        elif len(witness) == 4:
            R, M, n, P = witness
        elif len(witness) == 3:
            M, n, P = witness
            R = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: M is a maximal ideal of R
    h1 = False
    try:
        if hasattr(M, 'is_maximal'):
            val = M.is_maximal
            h1 = bool(val() if callable(val) else val)
        elif hasattr(M, 'is_maximal_ideal'):
            val = M.is_maximal_ideal
            h1 = bool(val() if callable(val) else val)
        elif R is not None and hasattr(R, 'is_maximal'):
            h1 = bool(R.is_maximal(M))
        elif isinstance(M, (int, sympy.Integer)):
            h1 = sympy.isprime(M)
    except Exception:
        pass

    # H_2: n is a positive integer
    h2 = False
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        pass

    # H_3: P is a prime ideal of R such that M^n is a subset of P
    h3_prime = False
    try:
        if hasattr(P, 'is_prime'):
            val = P.is_prime
            h3_prime = bool(val() if callable(val) else val)
        elif hasattr(P, 'is_prime_ideal'):
            val = P.is_prime_ideal
            h3_prime = bool(val() if callable(val) else val)
        elif R is not None and hasattr(R, 'is_prime'):
            h3_prime = bool(R.is_prime(P))
        elif isinstance(P, (int, sympy.Integer)):
            h3_prime = sympy.isprime(P) or P == 0
    except Exception:
        pass

    h3_subset = False
    try:
        Mn = M**n
        if hasattr(Mn, 'issubset'):
            h3_subset = bool(Mn.issubset(P))
        elif hasattr(Mn, 'is_subset'):
            h3_subset = bool(Mn.is_subset(P))
        elif hasattr(Mn, 'subset'):
            h3_subset = bool(Mn.subset(P))
        elif hasattr(P, 'contains'):
            h3_subset = bool(P.contains(Mn))
        elif hasattr(P, 'issuperset'):
            h3_subset = bool(P.issuperset(Mn))
        else:
            try:
                h3_subset = bool(Mn <= P)
            except Exception:
                pass
                
        if not h3_subset and isinstance(M, (int, sympy.Integer)) and isinstance(P, (int, sympy.Integer)):
            h3_subset = (Mn % P == 0) if P != 0 else (Mn == 0)
    except Exception:
        pass

    h3 = h3_prime and h3_subset

    # ¬Q: P is not equal to M
    neg_q = False
    try:
        neg_q = bool(P != M)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "H_2: n is a positive integer",
    "H_3: P is a prime ideal of R such that M^n is a subset of P",
    "¬Q: P is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3