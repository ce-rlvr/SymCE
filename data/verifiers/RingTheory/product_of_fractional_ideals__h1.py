import sympy
from sympy import *
import sympy.combinatorics as comb
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # 1. Check if witness is a dictionary containing pre-evaluated conditions
    if isinstance(witness, dict):
        if "neg_Q" in witness or "H1" in witness:
            return [
                bool(witness.get("H1", False)),
                bool(witness.get("H2", False)),
                bool(witness.get("H3", False)),
                bool(witness.get("neg_Q", False))
            ]
            
    # 2. Check if witness is an object with pre-evaluated conditions as attributes
    if hasattr(witness, "neg_Q") or hasattr(witness, "H1"):
        return [
            bool(getattr(witness, "H1", False)),
            bool(getattr(witness, "H2", False)),
            bool(getattr(witness, "H3", False)),
            bool(getattr(witness, "neg_Q", False))
        ]

    # 3. Check if witness is an object with specific evaluation methods
    try:
        h1 = bool(witness.K_is_field_of_fractions())
    except Exception:
        h1 = False
    try:
        h2 = bool(witness.I_is_fractional_ideal())
    except Exception:
        h2 = False
    try:
        h3 = bool(witness.J_is_fractional_ideal())
    except Exception:
        h3 = False
    try:
        neg_q = not bool(witness.IJ_is_fractional_ideal())
    except Exception:
        neg_q = False
        
    if any([h1, h2, h3, neg_q]):
        return [h1, h2, h3, neg_q]

    # 4. Otherwise, assume witness is a tuple (R, K, I, J) or an object with these attributes
    try:
        if hasattr(witness, "R") and hasattr(witness, "K"):
            R = witness.R
            K = witness.K
            I = witness.I
            J = witness.J
        else:
            R, K, I, J = witness
    except Exception:
        return [False, False, False, False]

    # Evaluate H1: K is the field of fractions of R
    h1 = False
    try:
        if hasattr(K, "is_field_of_fractions"):
            h1 = bool(K.is_field_of_fractions(R))
        elif hasattr(R, "frac_field"):
            h1 = (K == R.frac_field())
        elif hasattr(R, "field_of_fractions"):
            h1 = (K == R.field_of_fractions())
        elif callable(getattr(witness, "is_field_of_fractions", None)):
            h1 = bool(witness.is_field_of_fractions(K, R))
    except Exception:
        pass

    # Evaluate H2: I is a fractional ideal of R
    h2 = False
    try:
        if hasattr(I, "is_fractional_ideal"):
            h2 = bool(I.is_fractional_ideal(R))
        elif callable(getattr(witness, "is_fractional_ideal", None)):
            h2 = bool(witness.is_fractional_ideal(I, R))
    except Exception:
        pass

    # Evaluate H3: J is a fractional ideal of R
    h3 = False
    try:
        if hasattr(J, "is_fractional_ideal"):
            h3 = bool(J.is_fractional_ideal(R))
        elif callable(getattr(witness, "is_fractional_ideal", None)):
            h3 = bool(witness.is_fractional_ideal(J, R))
    except Exception:
        pass

    # Evaluate neg_Q: The product IJ is NOT a fractional ideal of R
    neg_q = False
    try:
        if hasattr(witness, "product"):
            IJ = witness.product(I, J)
        else:
            IJ = I * J
            
        if hasattr(IJ, "is_fractional_ideal"):
            neg_q = not bool(IJ.is_fractional_ideal(R))
        elif callable(getattr(witness, "is_fractional_ideal", None)):
            neg_q = not bool(witness.is_fractional_ideal(IJ, R))
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: I is a fractional ideal of R",
    "H_3: J is a fractional ideal of R",
    "¬Q: The product IJ is not a fractional ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3