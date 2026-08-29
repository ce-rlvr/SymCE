import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # The witness represents the integer n for the n-th root of unity.
        n = int(witness)
        h1_ok = (n == witness) and (n >= 1)
    except Exception:
        h1_ok = False

    try:
        # tau is defined as the complex conjugation automorphism on C.
        # This is a definitional hypothesis, so it holds for any valid n.
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        n = int(witness)
        # The conclusion states that the restriction of tau to Q(zeta_n) 
        # is a non-trivial Galois automorphism of order 2.
        # This fails if tau restricted to Q(zeta_n) is the identity (trivial, order 1).
        # Q(zeta_n) is a real field if and only if n = 1 or n = 2.
        # For n >= 3, Q(zeta_n) is totally complex and tau has order 2.
        neg_q_ok = (n == 1 or n == 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in C",
    "H_2: tau is the complex conjugation automorphism on C",
    "¬Q: The restriction of tau to Q(zeta_n) is not a non-trivial Galois automorphism of order 2"
]

N_HYP = 2
NEG_Q_INDEX = 2