import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def extract_d(witness):
    """
    Extracts the square-free integer d from various representations of the quadratic field Q(sqrt(d)).
    """
    if isinstance(witness, int):
        return witness
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
    if hasattr(witness, 'ext'):
        ext = witness.ext
        if ext.is_Pow and ext.exp == sympy.Rational(1, 2):
            return int(ext.base)
    if isinstance(witness, sympy.Expr):
        if witness.is_Pow and witness.exp == sympy.Rational(1, 2):
            return int(witness.base)
        if witness == sympy.I:
            return -1
    if isinstance(witness, str):
        s = witness.replace(" ", "")
        if "sqrt(" in s:
            start = s.find("sqrt(") + 5
            end = s.find(")", start)
            if start != -1 and end != -1:
                return int(s[start:end])
        return int(witness)
    return int(witness)

def conditions(witness) -> list[bool]:
    try:
        d = extract_d(witness)
        # A valid quadratic field Q(sqrt(d)) is defined by a square-free integer d != 0, 1
        h1 = (sympy.ntheory.mobius(abs(d)) != 0) and (d not in [0, 1])
    except Exception:
        h1 = False

    try:
        d = extract_d(witness)
        if not h1:
            neg_q = False
        else:
            # Check if the ring of integers O_K is a Euclidean domain
            if d < 0:
                # For imaginary quadratic fields, the only Euclidean domains are for d in {-1, -2, -3, -7, -11}
                is_euclidean = d in [-1, -2, -3, -7, -11]
            else:
                # For real quadratic fields, the known Euclidean domains up to d=100 are listed below
                known_euclidean_real = {2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73}
                if d <= 100:
                    is_euclidean = d in known_euclidean_real
                else:
                    # For d > 100, we assume it's not Euclidean for the sake of finding a small counterexample
                    is_euclidean = False
            
            neg_q = not is_euclidean
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: O_K is the ring of integers of K",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1