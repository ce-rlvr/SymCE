import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    Given a witness object, evaluates the remaining hypotheses and the negated conclusion.
    The witness is expected to be a dictionary, tuple, or object providing:
      - is_proper_ideal: bool
      - associated_primes: iterable of prime ideals
      - support: iterable of prime ideals
    """
    h1_ok = False
    neg_q_ok = False

    # 1. Try dictionary format
    if isinstance(witness, dict):
        try:
            h1_ok = bool(witness.get('is_proper_ideal', False))
        except Exception:
            pass
        try:
            ass = witness.get('associated_primes', [])
            supp = witness.get('support', [])
            # Negated conclusion: NOT (every associated prime belongs to the support)
            # i.e., there is an associated prime that is NOT in the support.
            neg_q_ok = any(p not in supp for p in ass)
        except Exception:
            pass
        return [h1_ok, neg_q_ok]

    # 2. Try tuple format: (is_proper_ideal, associated_primes, support)
    if isinstance(witness, tuple) and len(witness) == 3:
        try:
            h1_ok = bool(witness[0])
        except Exception:
            pass
        try:
            ass = witness[1]
            supp = witness[2]
            neg_q_ok = any(p not in supp for p in ass)
        except Exception:
            pass
        return [h1_ok, neg_q_ok]

    # 3. Try object format
    try:
        if hasattr(witness, 'is_proper_ideal'):
            prop = witness.is_proper_ideal
            h1_ok = bool(prop() if callable(prop) else prop)
    except Exception:
        h1_ok = False

    try:
        if hasattr(witness, 'associated_primes') and hasattr(witness, 'support'):
            ass = witness.associated_primes
            ass = ass() if callable(ass) else ass
            
            supp = witness.support
            supp = supp() if callable(supp) else supp
            
            neg_q_ok = any(p not in supp for p in ass)
    except Exception:
        neg_q_ok = False

    # 4. Fallback for sympy Ideal objects (can only evaluate H1)
    if not h1_ok:
        try:
            from sympy.polys.rings import Ideal
            if isinstance(witness, Ideal):
                h1_ok = not witness.is_whole_ring
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: There exists an associated prime ideal of R/I that does not belong to the support of R/I"
]

N_HYP = 1
NEG_Q_INDEX = 1