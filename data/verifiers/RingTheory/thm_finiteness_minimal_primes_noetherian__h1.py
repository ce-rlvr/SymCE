import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
    """
    Checks if the witness is a counterexample to the conjecture:
    "Assume R is a Noetherian ring. Let I be a proper ideal of R.
     Then there are only finitely many minimal prime ideals over I."
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness
            I = None
    except Exception:
        R = witness
        I = None

    # H_1: R is a Noetherian ring
    h1 = False
    try:
        if hasattr(R, 'is_noetherian'):
            h1 = bool(R.is_noetherian() if callable(R.is_noetherian) else R.is_noetherian)
        elif hasattr(R, 'is_Noetherian'):
            h1 = bool(R.is_Noetherian)
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R.domain, 'is_Field') and R.domain.is_Field:
            h1 = True
        elif R in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif isinstance(R, str):
            s = R.lower()
            if "noetherian" in s or "chatters" in s or "weyl" in s:
                h1 = True
    except Exception:
        pass

    # H_2: I is a proper ideal of R
    h2 = False
    try:
        if I is None:
            if isinstance(witness, str):
                s = witness.lower()
                if "proper" in s or "ideal" in s:
                    h2 = True
        else:
            if hasattr(I, 'is_proper_ideal'):
                h2 = bool(I.is_proper_ideal(R) if callable(I.is_proper_ideal) else I.is_proper_ideal)
            elif hasattr(I, 'is_proper'):
                h2 = bool(I.is_proper() if callable(I.is_proper) else I.is_proper)
            elif I == 0 or I == [0] or I == {0} or I == set([0]):
                h2 = True
            elif hasattr(I, 'contains') and hasattr(R, 'one'):
                h2 = not I.contains(R.one)
            elif isinstance(I, str):
                s = I.lower()
                if "proper" in s or "ideal" in s or s == "0" or s == "{0}":
                    h2 = True
    except Exception:
        pass

    # ¬Q: There are infinitely many minimal prime ideals over I
    neg_q = False
    try:
        if hasattr(witness, 'has_infinite_minimal_primes'):
            val = witness.has_infinite_minimal_primes
            neg_q = bool(val() if callable(val) else val)
        elif hasattr(R, 'has_infinite_minimal_primes'):
            val = R.has_infinite_minimal_primes
            neg_q = bool(val(I) if callable(val) else val)
        elif hasattr(I, 'has_infinite_minimal_primes'):
            val = I.has_infinite_minimal_primes
            neg_q = bool(val() if callable(val) else val)
        elif isinstance(witness, str) and "infinite" in witness.lower() and "prime" in witness.lower():
            neg_q = True
        elif isinstance(R, str) and "infinite" in R.lower() and "prime" in R.lower():
            neg_q = True
        elif isinstance(I, str) and "infinite" in I.lower() and "prime" in I.lower():
            neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: R is a Noetherian ring",
    "H_2: I is a proper ideal of R",
    "¬Q: There are infinitely many minimal prime ideals over I"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2