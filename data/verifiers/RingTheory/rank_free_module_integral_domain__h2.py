import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.abc

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

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: M has two bases of different cardinalities (rank is not well-defined)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = None
    except Exception:
        R = witness
        M = None

    # Evaluate H_1: R is an integral domain
    try:
        if isinstance(R, str):
            w = R.lower()
            if "cohn" in w or "domain" in w or "zero ring" in w:
                h1 = True
        elif isinstance(R, dict):
            if "is_integral_domain" in R:
                h1 = bool(R["is_integral_domain"])
            elif "is_domain" in R:
                h1 = bool(R["is_domain"])
        elif hasattr(R, "is_integral_domain"):
            h1 = bool(R.is_integral_domain)
        elif hasattr(R, "is_domain") and R.is_domain is not None:
            h1 = bool(R.is_domain)
        elif (isinstance(R, int) and R == 0) or R == sympy.S.Zero:
            # The zero ring trivially has no zero divisors
            h1 = True
    except Exception:
        pass

    # Evaluate ¬Q: M has bases of different cardinalities (R does not have IBN)
    try:
        if M is not None:
            if isinstance(M, dict):
                if "has_unique_basis_cardinality" in M:
                    neg_q = not bool(M["has_unique_basis_cardinality"])
                elif "has_ibn" in M:
                    neg_q = not bool(M["has_ibn"])
            elif hasattr(M, "has_unique_basis_cardinality"):
                neg_q = not bool(M.has_unique_basis_cardinality)
            elif hasattr(M, "has_ibn"):
                neg_q = not bool(M.has_ibn)
                
        if not neg_q:
            if isinstance(R, str):
                w = R.lower()
                if "cohn" in w or "no ibn" in w or "zero ring" in w:
                    neg_q = True
            elif isinstance(R, dict):
                if "has_IBN" in R:
                    neg_q = not bool(R["has_IBN"])
                elif "has_ibn" in R:
                    neg_q = not bool(R["has_ibn"])
            elif hasattr(R, "has_IBN"):
                neg_q = not bool(R.has_IBN)
            elif hasattr(R, "has_ibn"):
                neg_q = not bool(R.has_ibn)
            elif (isinstance(R, int) and R == 0) or R == sympy.S.Zero:
                # The zero ring does not have the Invariant Basis Number property
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]