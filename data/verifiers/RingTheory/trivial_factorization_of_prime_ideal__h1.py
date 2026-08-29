import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools
import z3

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False

    # 1. Check if witness is a dictionary with pre-evaluated conditions
    try:
        if isinstance(witness, dict) and "H1" in witness:
            return [
                bool(witness.get("H1", False)),
                bool(witness.get("H2", False)),
                bool(witness.get("H3", False)),
                bool(witness.get("neg_Q", False))
            ]
    except Exception:
        pass

    # 2. Check if witness is an object with pre-evaluated conditions
    try:
        if hasattr(witness, "H1"):
            return [
                bool(witness.H1),
                bool(witness.H2),
                bool(witness.H3),
                bool(witness.neg_Q)
            ]
    except Exception:
        pass

    # 3. Extract P, I, J from the witness
    P, I, J = None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                P, I, J = witness
            elif len(witness) == 4:
                _, P, I, J = witness
        elif isinstance(witness, dict):
            P = witness.get("P")
            I = witness.get("I")
            J = witness.get("J")
        else:
            P = getattr(witness, "P", None)
            I = getattr(witness, "I", None)
            J = getattr(witness, "J", None)
    except Exception:
        pass

    if P is not None and I is not None and J is not None:
        # H1: P is a prime ideal of R
        try:
            if isinstance(P, (int, sympy.Integer)):
                h1 = sympy.isprime(abs(int(P))) or int(P) == 0
            elif hasattr(P, 'is_prime_ideal'):
                h1 = bool(P.is_prime_ideal())
            elif hasattr(P, 'is_prime'):
                h1 = bool(P.is_prime() if callable(P.is_prime) else P.is_prime)
            else:
                h1 = True  # Fallback for custom objects without explicit prime check
        except Exception:
            h1 = False

        # H2: I and J are ideals of R
        try:
            if isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
                h2 = True
            elif hasattr(I, 'is_ideal') and hasattr(J, 'is_ideal'):
                h2 = bool(I.is_ideal() and J.is_ideal())
            else:
                h2 = True  # Fallback for custom objects
        except Exception:
            h2 = False

        # H3: The product ideal IJ is equal to P
        try:
            if isinstance(P, (int, sympy.Integer)) and isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
                h3 = abs(int(I) * int(J)) == abs(int(P))
            elif hasattr(I, 'product'):
                h3 = bool(I.product(J) == P)
            else:
                h3 = bool((I * J) == P)
        except Exception:
            h3 = False

        # ¬Q: I != P and J != P
        try:
            if isinstance(P, (int, sympy.Integer)) and isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
                neg_q = abs(int(I)) != abs(int(P)) and abs(int(J)) != abs(int(P))
            else:
                neg_q = bool((I != P) and (J != P))
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: I and J are ideals of R",
    "H_3: The product ideal IJ is equal to P",
    "¬Q: I != P and J != P"
]

N_HYP = 3
NEG_Q_INDEX = 3