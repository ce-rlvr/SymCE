import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be an object representing a ring and an ideal,
    or providing methods/properties to check the conditions directly, as SymPy 
    does not natively support non-commutative ideal operations.
    """
    # H_1: P is a prime ideal of R
    try:
        if callable(getattr(witness, 'is_prime_ideal', None)):
            h1_ok = bool(witness.is_prime_ideal())
        elif hasattr(witness, 'is_prime_ideal'):
            h1_ok = bool(witness.is_prime_ideal)
        elif isinstance(witness, dict) and 'is_prime_ideal' in witness:
            h1_ok = bool(witness['is_prime_ideal'])
        elif hasattr(witness, 'is_prime'):
            h1_ok = bool(witness.is_prime())
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion FAILS at the witness.
    # Conclusion: P is a minimal prime ideal iff for every x in P, there exists y not in P and n >= 1 such that y x^n = 0.
    try:
        # Check if P is a minimal prime ideal
        if callable(getattr(witness, 'is_minimal_prime_ideal', None)):
            is_minimal = bool(witness.is_minimal_prime_ideal())
        elif hasattr(witness, 'is_minimal_prime_ideal'):
            is_minimal = bool(witness.is_minimal_prime_ideal)
        elif isinstance(witness, dict) and 'is_minimal_prime_ideal' in witness:
            is_minimal = bool(witness['is_minimal_prime_ideal'])
        elif hasattr(witness, 'is_minimal'):
            is_minimal = bool(witness.is_minimal())
        else:
            is_minimal = False

        # Check if the condition holds: for every x in P, exists y not in P, n >= 1 st y x^n = 0
        if callable(getattr(witness, 'satisfies_condition', None)):
            condition_holds = bool(witness.satisfies_condition())
        elif hasattr(witness, 'satisfies_condition'):
            condition_holds = bool(witness.satisfies_condition)
        elif isinstance(witness, dict) and 'satisfies_condition' in witness:
            condition_holds = bool(witness['satisfies_condition'])
        elif callable(getattr(witness, 'condition_holds', None)):
            condition_holds = bool(witness.condition_holds())
        else:
            condition_holds = False

        # The conclusion is the logical equivalence (is_minimal <==> condition_holds)
        # The negated conclusion is True when the equivalence fails (i.e., XOR)
        neg_q_ok = (is_minimal != condition_holds)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P is a minimal prime ideal if and only if for every element x in P, there exists an element y in R \\ P and an integer n >= 1 such that y x^n = 0 is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1