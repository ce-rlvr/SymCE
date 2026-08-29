import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import *

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
    Check if the witness is a counterexample to the false conjecture.
    The dropped hypothesis is that f is a polynomial.
    """
    # H_1: R is a commutative ring
    try:
        # We interpret this as the witness being a scalar expression 
        # belonging to a commutative ring (all free symbols commute).
        if isinstance(witness, sp.Expr) and not getattr(witness, 'is_Matrix', False):
            h1 = all(s.is_commutative for s in witness.free_symbols)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: f cannot be uniquely written as a finite sum of non-zero homogeneous polynomials,
    # each having a distinct total degree.
    try:
        if isinstance(witness, sp.Expr) and not getattr(witness, 'is_Matrix', False):
            syms = list(witness.free_symbols)
            if not syms:
                is_poly = True
            else:
                is_poly = witness.is_polynomial(*syms)
                if not is_poly:
                    # Try a basic simplification in case it's an unsimplified polynomial
                    is_poly = sp.cancel(witness).is_polynomial(*syms)
            neg_q = not is_poly
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: f cannot be uniquely written as a finite sum of non-zero homogeneous polynomials of distinct degrees"
]

N_HYP = 1
NEG_Q_INDEX = 1