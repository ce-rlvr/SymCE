import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for an integral domain R, K \otimes_R K is isomorphic to K.
    This is true if K is the field of fractions of a commutative domain R.
    It fails if K is a proper extension of the field of fractions, or if R is non-commutative.
    """
    # Unpack witness. It could be a tuple (R, K) or just R.
    if isinstance(witness, tuple) and len(witness) == 2:
        R, K = witness
    else:
        R = witness
        K = None

    # H_1: R is an integral domain
    try:
        if R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        elif hasattr(R, 'is_domain'):
            h1 = bool(R.is_domain)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The tensor product K \otimes_R K is not isomorphic to K as an R-module
    try:
        neg_q = False
        if K is not None:
            # If K is provided, check if it's a proper extension (degree/rank > 1)
            if hasattr(K, 'degree'):
                d = K.degree() if callable(K.degree) else K.degree
                if d > 1:
                    neg_q = True
            elif hasattr(K, 'rank'):
                r = K.rank() if callable(K.rank) else K.rank
                if r > 1:
                    neg_q = True
            elif isinstance(K, int):
                if K > 1:
                    neg_q = True
            elif K in (sympy.S.Complexes, sympy.polys.domains.CC) and R in (sympy.S.Reals, sympy.polys.domains.RR):
                neg_q = True
            elif K in (sympy.S.Reals, sympy.polys.domains.RR) and R in (sympy.S.Integers, sympy.polys.domains.ZZ):
                neg_q = True
            elif K in (sympy.S.Complexes, sympy.polys.domains.CC) and R in (sympy.S.Integers, sympy.polys.domains.ZZ):
                neg_q = True
            elif K in (sympy.S.Reals, sympy.polys.domains.RR) and R in (sympy.S.Rationals, sympy.polys.domains.QQ):
                neg_q = True
            elif K in (sympy.S.Complexes, sympy.polys.domains.CC) and R in (sympy.S.Rationals, sympy.polys.domains.QQ):
                neg_q = True
            elif hasattr(K, 'dimension'):
                dim = K.dimension() if callable(K.dimension) else K.dimension
                if dim > 1:
                    neg_q = True
            elif isinstance(K, (list, tuple)):
                if len(K) > 1:
                    neg_q = True
        else:
            # If K is not provided, assume K is the field of fractions.
            # Then K \otimes_R K \cong K fails only if R is non-commutative.
            if hasattr(R, 'is_commutative'):
                if not R.is_commutative:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The tensor product K \\otimes_R K is not isomorphic to K as an R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1