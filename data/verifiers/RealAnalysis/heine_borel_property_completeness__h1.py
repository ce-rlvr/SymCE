import sympy
from sympy import Set, Matrix, S, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
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

CONDITION_LABELS = [
    "H_1: Every closed and bounded subset of X is compact",
    "¬Q: The metric space (X, d) is not complete"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    For subsets of R (the standard domain for such witnesses), the Heine-Borel 
    property holds if and only if the subset is closed in R. 
    Similarly, a subset of R is complete if and only if it is closed in R.
    """
    h1 = False
    neg_q = False
    
    # Handle string representations
    if isinstance(witness, str):
        w = witness.lower().strip()
        if w in ["q", "rationals", "rational", "s.rationals"]:
            return [False, True]
        elif w in ["r", "reals", "real", "s.reals"]:
            return [True, False]
        elif w in ["z", "integers", "integer", "s.integers"]:
            return [True, False]
        elif w in ["n", "naturals", "natural", "s.naturals"]:
            return [True, False]
        return [False, False]

    # Handle SymPy singletons
    if witness == S.Rationals:
        return [False, True]
    if witness in (S.Reals, S.Integers, S.Naturals, S.Naturals0):
        return [True, False]

    # Handle finite metric spaces (represented as lists, tuples, or matrices)
    if isinstance(witness, (list, tuple, Matrix)):
        # Finite metric spaces are always complete, and all their subsets are compact.
        return [True, False]

    # Handle SymPy Sets (subsets of Reals)
    if isinstance(witness, Set):
        try:
            is_closed = witness.is_closed
            if is_closed is True:
                h1 = True
                neg_q = False
            elif is_closed is False:
                h1 = False
                neg_q = True
            else:
                h1 = False
                neg_q = False
        except Exception:
            h1 = False
            neg_q = False
        return [h1, neg_q]

    return [False, False]