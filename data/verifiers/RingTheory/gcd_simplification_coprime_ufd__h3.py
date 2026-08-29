import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
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
    # H_1: R is a unique factorization domain
    try:
        h1_ok = isinstance(witness, (tuple, list)) and len(witness) == 3
        if h1_ok:
            for elem in witness:
                # Integers and sympy expressions (like polynomials) belong to UFDs
                if not isinstance(elem, (int, sympy.Integer, sympy.Expr)):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: a, b, c are non-zero elements of R
    try:
        h2_ok = True
        if h1_ok:
            for elem in witness:
                if elem == 0:
                    h2_ok = False
                    break
                if isinstance(elem, sympy.Expr) and sympy.simplify(elem).is_zero:
                    h2_ok = False
                    break
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: gcd(a, bc) and gcd(a, c) are not associates in R
    try:
        neg_q_ok = False
        if h1_ok:
            a, b, c = witness
            g1 = sympy.gcd(a, b * c)
            g2 = sympy.gcd(a, c)
            
            are_assoc = False
            # sympy.gcd returns canonical generators, so associates will be equal up to sign
            if g1 == g2 or g1 == -g2:
                are_assoc = True
            else:
                try:
                    if sympy.simplify(g1 - g2).is_zero or sympy.simplify(g1 + g2).is_zero:
                        are_assoc = True
                except Exception:
                    pass
            
            neg_q_ok = not are_assoc
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "¬Q: gcd(a, bc) and gcd(a, c) are not associates in R"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2